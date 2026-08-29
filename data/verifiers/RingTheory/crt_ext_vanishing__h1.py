import sympy
from sympy import Matrix, zeros, eye
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I and J are comaximal",
    "H_3: n >= 0 is an integer",
    "¬Q: The Ext group Ext^n_R(R/I, R/J) is not the trivial group"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_in_span(M, basis):
    if not basis:
        return M.is_zero_matrix
    v = M.vec()
    B = Matrix.hstack(*[b.vec() for b in basis])
    return B.rank() == B.row_join(v).rank()

def is_ring(R_basis):
    if not R_basis: return False
    R_mat = Matrix.hstack(*[r.vec() for r in R_basis])
    if R_mat.rank() != len(R_basis): return False
    for a in R_basis:
        for b in R_basis:
            if not is_in_span(a*b, R_basis): return False
    shape = R_basis[0].shape
    if shape[0] != shape[1]: return False
    I_mat = eye(shape[0])
    if not is_in_span(I_mat, R_basis): return False
    return True

def is_ideal(I_basis, R_basis):
    for i in I_basis:
        if not is_in_span(i, R_basis): return False
    for r in R_basis:
        for i in I_basis:
            if not is_in_span(r*i, I_basis): return False
            if not is_in_span(i*r, I_basis): return False
    return True

def are_comaximal(I_basis, J_basis, R_basis):
    basis = I_basis + J_basis
    for r in R_basis:
        if not is_in_span(r, basis): return False
    return True

def get_quotient_basis(R_basis, I_basis):
    basis = []
    if not I_basis:
        current_mat = zeros(R_basis[0].vec().shape[0], 0)
    else:
        current_mat = Matrix.hstack(*[m.vec() for m in I_basis])
    
    current_rank = current_mat.rank() if current_mat.shape[0] > 0 else 0
    
    for r in R_basis:
        v = r.vec()
        new_mat = current_mat.row_join(v) if current_mat.shape[0] > 0 else v
        new_rank = new_mat.rank()
        if new_rank > current_rank:
            basis.append(r)
            current_mat = new_mat
            current_rank = new_rank
    return basis

def get_representation(R_basis, I_basis):
    B_M = get_quotient_basis(R_basis, I_basis)
    dim = len(B_M)
    if dim == 0:
        return B_M, [zeros(0, 0) for _ in R_basis]
    
    sys_vecs = [b.vec() for b in B_M] + [i.vec() for i in I_basis]
    sys_mat = Matrix.hstack(*sys_vecs)
    
    rho = []
    for r in R_basis:
        mat = zeros(dim, dim)
        for j, b in enumerate(B_M):
            v = (r * b).vec()
            sol, _ = sys_mat.gauss_jordan_solve(v)
            for i in range(dim):
                mat[i, j] = sol[i]
        rho.append(mat)
    return B_M, rho

def get_multiplication_table(R_basis):
    m = len(R_basis)
    C = {}
    R_mat = Matrix.hstack(*[r.vec() for r in R_basis])
    for a in range(m):
        for b in range(m):
            v = (R_basis[a] * R_basis[b]).vec()
            sol, _ = R_mat.gauss_jordan_solve(v)
            C[(a, b)] = sol
    return C

def compute_ext_0(R_basis, I_basis, J_basis):
    B_M, rho_M = get_representation(R_basis, I_basis)
    B_N, rho_N = get_representation(R_basis, J_basis)
    
    d_M = len(B_M)
    d_N = len(B_N)
    m = len(R_basis)
    
    if d_M == 0 or d_N == 0:
        return 0
        
    B_mat = zeros(m * d_N * d_M, d_N * d_M)
    for k in range(m):
        for i in range(d_N):
            for j in range(d_M):
                row = k * (d_N * d_M) + i * d_M + j
                for u in range(d_N):
                    col = u * d_M + j
                    B_mat[row, col] += rho_N[k][i, u]
                for v in range(d_M):
                    col = i * d_M + v
                    B_mat[row, col] -= rho_M[k][v, j]
                    
    return d_N * d_M - B_mat.rank()

def compute_ext_1(R_basis, I_basis, J_basis):
    B_M, rho_M = get_representation(R_basis, I_basis)
    B_N, rho_N = get_representation(R_basis, J_basis)
    
    d_M = len(B_M)
    d_N = len(B_N)
    m = len(R_basis)
    
    if d_M == 0 or d_N == 0:
        return 0
        
    C = get_multiplication_table(R_basis)
    
    B_mat = zeros(m * d_N * d_M, d_N * d_M)
    for k in range(m):
        for i in range(d_N):
            for j in range(d_M):
                row = k * (d_N * d_M) + i * d_M + j
                for u in range(d_N):
                    col = u * d_M + j
                    B_mat[row, col] += rho_N[k][i, u]
                for v in range(d_M):
                    col = i * d_M + v
                    B_mat[row, col] -= rho_M[k][v, j]
                    
    dim_B1 = B_mat.rank()
    
    Z_mat = zeros(m * m * d_N * d_M, m * d_N * d_M)
    row_idx = 0
    for a in range(m):
        for b in range(m):
            for i in range(d_N):
                for j in range(d_M):
                    for k in range(m):
                        col = k * (d_N * d_M) + i * d_M + j
                        Z_mat[row_idx, col] += C[(a, b)][k]
                    for u in range(d_N):
                        col = b * (d_N * d_M) + u * d_M + j
                        Z_mat[row_idx, col] -= rho_N[a][i, u]
                    for v in range(d_M):
                        col = a * (d_N * d_M) + i * d_M + v
                        Z_mat[row_idx, col] -= rho_M[b][v, j]
                    row_idx += 1
                    
    dim_Z1 = m * d_N * d_M - Z_mat.rank()
    return dim_Z1 - dim_B1

def conditions(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 4:
            return [False, False, False, False]
        R_basis, I_basis, J_basis, n = witness
        
        h1 = is_ring(R_basis) and is_ideal(I_basis, R_basis) and is_ideal(J_basis, R_basis)
        h2 = are_comaximal(I_basis, J_basis, R_basis)
        h3 = isinstance(n, int) and n >= 0
        
        neg_q = False
        if h1 and h2 and h3:
            if n == 0:
                dim = compute_ext_0(R_basis, I_basis, J_basis)
                neg_q = (dim > 0)
            elif n == 1:
                dim = compute_ext_1(R_basis, I_basis, J_basis)
                neg_q = (dim > 0)
            else:
                neg_q = False
                
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]