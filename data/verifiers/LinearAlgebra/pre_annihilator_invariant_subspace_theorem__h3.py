import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        T, U = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        T_mat = sp.Matrix(T)
        h1_ok = T_mat.is_square
        h2_ok = T_mat.is_square
        n = T_mat.rows
    except Exception:
        h1_ok = False
        h2_ok = False
        n = 0

    try:
        if isinstance(U, (list, tuple)) and len(U) > 0 and isinstance(U[0], sp.MatrixBase):
            if U[0].cols == 1:
                U_mat = sp.Matrix.hstack(*U).T
            else:
                U_mat = sp.Matrix.vstack(*U)
        else:
            U_mat = sp.Matrix(U)
            
        if U_mat.rows == 0:
            U_mat = sp.zeros(0, n)
            h3_ok = True
        elif U_mat.cols != n:
            h3_ok = False
        else:
            rank_U = U_mat.rank()
            rank_UT = U_mat.col_join(U_mat * T_mat).rank()
            h3_ok = (rank_U == rank_UT)
    except Exception:
        h3_ok = False

    try:
        if not (h1_ok and h2_ok and h3_ok):
            neg_q = False
        else:
            N = U_mat.nullspace()
            if not N:
                neg_q = False
            else:
                N_mat = sp.Matrix.hstack(*N)
                res = sp.simplify(U_mat * T_mat * N_mat)
                neg_q = not res.is_zero_matrix
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: T is a linear operator on V",
    "H_3: U is a subspace of V^* that is invariant under T^*",
    "¬Q: The pre-annihilator ^0U is not invariant under T"
]

N_HYP = 3
NEG_Q_INDEX = 3