import sympy
from sympy import Matrix, eye, zeros, Symbol
import z3

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def are_similar_over_Q(A, B):
    n = A.shape[0]
    
    def kron(X, Y):
        rX, cX = X.shape
        rY, cY = Y.shape
        return Matrix(rX*rY, cX*cY, lambda i, j: X[i//rY, j//cY] * Y[i%rY, j%cY])
        
    I = eye(n)
    M = kron(A.T, I) - kron(I, B)
    null_basis = M.nullspace()
    if not null_basis:
        return False
        
    c = [Symbol(f'c{i}') for i in range(len(null_basis))]
    P = Matrix.zeros(n, n)
    for idx, vec in enumerate(null_basis):
        P_mat = Matrix(n, n, lambda i, j: vec[j*n + i, 0])
        P += c[idx] * P_mat
        
    det_poly = P.det().expand()
    return det_poly != 0

def are_conjugate_in_GLnZ(A, B):
    n = A.shape[0]
    solver = z3.Solver()
    
    P_vars = [[z3.Int(f'p_{i}_{j}') for j in range(n)] for i in range(n)]
    
    for i in range(n):
        for j in range(n):
            lhs = sum(P_vars[i][k] * int(A[k, j]) for k in range(n))
            rhs = sum(int(B[i][k]) * P_vars[k][j] for k in range(n))
            solver.add(lhs == rhs)
            
    def z3_det(matrix_vars):
        m = len(matrix_vars)
        if m == 1:
            return matrix_vars[0][0]
        if m == 2:
            return matrix_vars[0][0]*matrix_vars[1][1] - matrix_vars[0][1]*matrix_vars[1][0]
        det = 0
        for j in range(m):
            sub_matrix = [row[:j] + row[j+1:] for row in matrix_vars[1:]]
            sign = 1 if j % 2 == 0 else -1
            det += sign * matrix_vars[0][j] * z3_det(sub_matrix)
        return det

    det = z3_det(P_vars)
    solver.add(z3.Or(det == 1, det == -1))
    
    return solver.check() == z3.sat

def is_int_matrix(M):
    for val in M:
        if getattr(val, 'is_integer', False) != True:
            return False
    return True

def conditions(witness):
    try:
        A, B = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: n is a positive integer
    try:
        h1 = hasattr(A, 'shape') and hasattr(B, 'shape') and \
             A.shape[0] == A.shape[1] and B.shape[0] == B.shape[1] and \
             A.shape[0] == B.shape[0] and A.shape[0] > 0
    except Exception:
        h1 = False
        
    # H2: A is a matrix in the general linear group GL_n(F)
    try:
        if h1 and is_int_matrix(A):
            detA = A.det()
            h2 = (detA == 1 or detA == -1)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: B is a matrix in the general linear group GL_n(F)
    try:
        if h1 and is_int_matrix(B):
            detB = B.det()
            h3 = (detB == 1 or detB == -1)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: A and B have the same rational canonical form but are not conjugate in GL_n(F)
    try:
        if h1 and h2 and h3:
            same_rcf = are_similar_over_Q(A, B)
            conjugate = are_conjugate_in_GLnZ(A, B)
            neg_q = same_rcf and not conjugate
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: A is a matrix in the general linear group GL_n(F)",
    "H_3: B is a matrix in the general linear group GL_n(F)",
    "¬Q: A and B have the same rational canonical form but are not conjugate in GL_n(F)"
]

N_HYP = 3
NEG_Q_INDEX = 3