import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import z3

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    A, B = None, None
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
        elif isinstance(witness, tuple) and len(witness) >= 2:
            A, B = witness[-2], witness[-1]
            
        if A is not None and not isinstance(A, sp.MatrixBase):
            A = sp.Matrix(A)
        if B is not None and not isinstance(B, sp.MatrixBase):
            B = sp.Matrix(B)
    except Exception:
        pass

    def is_int(x):
        return (hasattr(x, 'is_Integer') and x.is_Integer) or isinstance(x, int)

    # H1: n is a positive integer
    try:
        h1 = bool(A is not None and B is not None and 
                  hasattr(A, 'is_square') and A.is_square and 
                  hasattr(B, 'is_square') and B.is_square and 
                  A.shape == B.shape and A.shape[0] > 0)
    except Exception:
        h1 = False

    # H2: GL_n(F) is the general linear group of degree n over F
    # This is a definitional hypothesis.
    h2 = True

    # H3: A and B are matrices in GL_n(F)
    try:
        if h1:
            # If matrices are over Z, they are in GL_n(Z) iff their determinant is ±1
            if all(is_int(x) for x in A) and all(is_int(x) for x in B):
                h3 = bool(A.det() in [1, -1] and B.det() in [1, -1])
            else:
                # Over a field, they are in GL_n(F) iff their determinant is non-zero
                h3 = bool(A.det() != 0 and B.det() != 0)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: A and B are conjugate in GL_n(F) if and only if they have the same rational canonical form
    # The conclusion fails if they have the same RCF but are NOT conjugate in GL_n(F).
    try:
        if not h1:
            neg_q = False
        else:
            same_rcf = bool(A.is_similar(B))
            
            if all(is_int(x) for x in A) and all(is_int(x) for x in B):
                n = A.shape[0]
                solver = z3.Solver()
                P = [[z3.Int(f'p_{i}_{j}') for j in range(n)] for i in range(n)]
                
                for i in range(n):
                    for j in range(n):
                        lhs = sum(P[i][k] * int(A[k, j]) for k in range(n))
                        rhs = sum(int(B[i][k]) * P[k][j] for k in range(n))
                        solver.add(lhs == rhs)
                        
                def z3_det(matrix):
                    m = len(matrix)
                    if m == 1:
                        return matrix[0][0]
                    if m == 2:
                        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
                    det = 0
                    for c in range(m):
                        sub_matrix = [row[:c] + row[c+1:] for row in matrix[1:]]
                        sign = 1 if c % 2 == 0 else -1
                        det += sign * matrix[0][c] * z3_det(sub_matrix)
                    return det

                det = z3_det(P)
                solver.add(z3.Or(det == 1, det == -1))
                
                conjugate = (solver.check() == z3.sat)
            else:
                conjugate = bool(A.is_similar(B))
                
            neg_q = bool(conjugate != same_rcf)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]


CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: GL_n(F) is the general linear group of degree n over F",
    "H_3: A and B are matrices in GL_n(F)",
    "¬Q: A and B have the same rational canonical form but are not conjugate in GL_n(F)"
]

N_HYP = 3
NEG_Q_INDEX = 3