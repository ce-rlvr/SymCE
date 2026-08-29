import sympy
from sympy import Matrix

# Top-level setup
# The witness should be a tuple (R_basis, I_basis, J_basis) or (R_basis, I_basis, J_basis, n)
# where R_basis, I_basis, J_basis are lists of sympy.Matrix objects of the same shape.
# They represent the basis of the ring R and its ideals I, J as algebras over a field.
# A known counterexample uses a commutative rng with zero multiplication.
N1 = Matrix([[0, 1, 0], [0, 0, 0], [0, 0, 0]])
N2 = Matrix([[0, 0, 1], [0, 0, 0], [0, 0, 0]])
N3 = Matrix([[0, 0, 0], [0, 0, 1], [0, 0, 0]])
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_span_rank(basis):
    if not basis: return 0
    M = sympy.Matrix.hstack(*[b.vec() for b in basis])
    return M.rank()

def span_contains(basis, target):
    if all(x == 0 for x in target): return True
    if not basis: return False
    M = sympy.Matrix.hstack(*[b.vec() for b in basis])
    M_aug = sympy.Matrix.hstack(M, target.vec())
    return M.rank() == M_aug.rank()

def spans_eq(basis1, basis2):
    if not basis1 and not basis2: return True
    r1 = get_span_rank(basis1)
    r2 = get_span_rank(basis2)
    if r1 != r2: return False
    r_union = get_span_rank(basis1 + basis2)
    return r1 == r_union

def is_commutative_ring(R_basis):
    try:
        for a in R_basis:
            if not a.is_square:
                return False
            for b in R_basis:
                ab = a * b
                ba = b * a
                if ab != ba:
                    return False
                if not span_contains(R_basis, ab):
                    return False
        return True
    except Exception:
        return False

def is_ideal(R_basis, I_basis):
    try:
        for i in I_basis:
            if not span_contains(R_basis, i):
                return False
        for r in R_basis:
            for i in I_basis:
                if not span_contains(I_basis, r * i):
                    return False
        return True
    except Exception:
        return False

def is_comaximal(R_basis, I_basis, J_basis):
    try:
        return spans_eq(R_basis, I_basis + J_basis)
    except Exception:
        return False

def get_independent_basis(basis):
    if not basis: return []
    vecs = [b.vec() for b in basis]
    M = sympy.Matrix.hstack(*vecs)
    rref_matrix, pivot_cols = M.rref()
    return [basis[i] for i in pivot_cols]

def get_quotient_basis(V_basis, W_basis):
    q_basis = []
    if not V_basis: return []
    
    W_vecs = [w.vec() for w in W_basis]
    
    if not W_vecs:
        current_M = sympy.Matrix(V_basis[0].vec().shape[0], 0, [])
        current_rank = 0
    else:
        current_M = sympy.Matrix.hstack(*W_vecs)
        current_rank = current_M.rank()
        
    for v in V_basis:
        v_vec = v.vec()
        new_M = sympy.Matrix.hstack(current_M, v_vec)
        new_rank = new_M.rank()
        if new_rank > current_rank:
            q_basis.append(v)
            current_M = new_M
            current_rank = new_rank
    return q_basis

def get_action_matrix(r, q_basis, W_indep_basis):
    d = len(q_basis)
    if d == 0:
        return sympy.zeros(0, 0)
    
    basis_vecs = [b.vec() for b in q_basis] + [w.vec() for w in W_indep_basis]
    M = sympy.Matrix.hstack(*basis_vecs)
    
    A = sympy.zeros(d, d)
    for j, q in enumerate(q_basis):
        rq = r * q
        x = M.solve(rq.vec())
        for i in range(d):
            A[i, j] = x[i]
    return A

def is_hom_trivial(R_basis, I_basis, J_basis):
    I_indep = get_independent_basis(I_basis)
    J_indep = get_independent_basis(J_basis)
    
    qI_basis = get_quotient_basis(R_basis, I_indep)
    qJ_basis = get_quotient_basis(R_basis, J_indep)
    
    d1 = len(qI_basis)
    d2 = len(qJ_basis)
    
    if d1 == 0 or d2 == 0:
        return True
        
    Sys_rows = []
    for r in R_basis:
        A = get_action_matrix(r, qI_basis, I_indep)
        B = get_action_matrix(r, qJ_basis, J_indep)
        
        for i in range(d2):
            for j in range(d1):
                row = [0] * (d2 * d1)
                for k in range(d2):
                    row[k * d1 + j] += B[i, k]
                for k in range(d1):
                    row[i * d1 + k] -= A[k, j]
                Sys_rows.append(row)
                
    if not Sys_rows:
        return False
        
    Sys = sympy.Matrix(Sys_rows)
    return Sys.rank() == d2 * d1

def conditions(witness):
    try:
        if len(witness) == 3:
            R_basis, I_basis, J_basis = witness
            n = 0
        elif len(witness) == 4:
            R_basis, I_basis, J_basis, n = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = is_commutative_ring(R_basis)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ideal(R_basis, I_basis) and is_ideal(R_basis, J_basis)
    except Exception:
        h2 = False
        
    try:
        h3 = is_comaximal(R_basis, I_basis, J_basis)
    except Exception:
        h3 = False
        
    try:
        if n == 0:
            neg_q = not is_hom_trivial(R_basis, I_basis, J_basis)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "H_3: I and J are comaximal",
    "¬Q: Ext^n_R(R/I, R/J) is not the trivial group"
]

N_HYP = 3
NEG_Q_INDEX = 3