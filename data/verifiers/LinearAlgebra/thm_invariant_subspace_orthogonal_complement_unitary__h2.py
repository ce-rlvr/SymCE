import sympy
from sympy import Matrix, eye, zeros, simplify

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat(m):
    for e in m:
        if e == 0:
            continue
        e_exp = e.expand()
        if e_exp == 0:
            continue
        e_simp = simplify(e_exp)
        if e_simp == 0:
            continue
        return False
    return True

def conditions(witness):
    try:
        U, W = witness
    except Exception:
        return [False, False]
    
    try:
        if not isinstance(U, Matrix):
            h1 = False
        elif not U.is_square:
            h1 = False
        else:
            n = U.shape[0]
            diff = U.H * U - eye(n)
            h1 = is_zero_mat(diff)
            
            if isinstance(W, list):
                if len(W) > 0:
                    W_mat = Matrix.hstack(*[Matrix(w) for w in W])
                else:
                    W_mat = zeros(n, 1)
            elif isinstance(W, Matrix):
                W_mat = W
            else:
                h1 = False
                
            if h1 and W_mat.shape[0] != n:
                h1 = False
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            W_perp_basis = W_mat.H.nullspace()
            is_invariant = True
            for v in W_perp_basis:
                prod = W_mat.H * (U * v)
                if not is_zero_mat(prod):
                    is_invariant = False
                    break
            neg_q = not is_invariant
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix operating on a finite-dimensional complex inner product space V",
    "¬Q: The orthogonal complement of W is not invariant under U"
]

N_HYP = 1
NEG_Q_INDEX = 1