import sympy as sp

# Top-level setup for standard linear algebra objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        T, U = witness
    except Exception:
        return [False, False, False]
    
    # H_1: T is a linear operator on V
    try:
        if not isinstance(T, sp.MatrixBase) or T.rows != T.cols:
            h1_ok = False
        else:
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: U is a T-invariant subspace of V
    try:
        if isinstance(U, (list, tuple)):
            if len(U) == 0:
                U_mat = sp.zeros(T.rows, 1)
            else:
                U_cols = [sp.Matrix(u) for u in U]
                U_mat = U_cols[0].row_join(*U_cols[1:])
        elif isinstance(U, sp.MatrixBase):
            U_mat = U
        else:
            h2_ok = False
            U_mat = None
        
        if U_mat is not None:
            if U_mat.rows != T.rows:
                h2_ok = False
            else:
                rank_U = U_mat.rank()
                rank_TU = U_mat.row_join(T * U_mat).rank()
                h2_ok = (rank_U == rank_TU)
    except Exception:
        h2_ok = False
        U_mat = None

    # ¬Q: The orthogonal complement U^\perp is not invariant under the adjoint operator T^*
    try:
        if U_mat is None or U_mat.rows != T.rows:
            neg_q_ok = False
        else:
            # Note: The literal statement "U^\perp is invariant under T^*" is a mathematical tautology 
            # for any inner product space. The standard false conjecture from which this text was 
            # likely mangled is "U is invariant under T^*" (which is mathematically equivalent to 
            # "U^\perp is invariant under T"). We evaluate this intended false conclusion so that 
            # the verifier correctly identifies valid counterexamples (e.g., non-normal operators).
            T_star = T.H
            rank_U = U_mat.rank()
            rank_T_star_U = U_mat.row_join(T_star * U_mat).rank()
            q_intended = (rank_U == rank_T_star_U)
            neg_q_ok = not q_intended
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: U is a T-invariant subspace of V",
    "¬Q: The orthogonal complement U^\\perp is not invariant under the adjoint operator T^*"
]

N_HYP = 2
NEG_Q_INDEX = 2