import sympy as sp

# Top-level setup for standard named objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (B, T) representing matrices for the bilinear form B 
    and the linear operator T, this function checks the hypotheses and the 
    negated conclusion of the conjecture.
    """
    try:
        B, T = witness
    except Exception:
        return [False, False, False, False]

    # H_1: B is a non-degenerate bilinear form on V
    try:
        h1_ok = bool(B.det() != 0)
    except Exception:
        h1_ok = False

    # H_2: T is an invertible linear operator on V
    try:
        h2_ok = bool(T.det() != 0)
    except Exception:
        h2_ok = False

    # H_3: T is self-adjoint with respect to B, meaning T^* = T
    # The adjoint T^* with respect to a bilinear form B satisfies B(Tx, y) = B(x, T^*y).
    # In matrix notation, this means T^T B = B T^*, so T^* = B^{-1} T^T B.
    # T is self-adjoint if T^* = T, which is equivalent to T^T B = B T.
    try:
        h3_ok = bool((T.transpose() * B) == (B * T))
    except Exception:
        h3_ok = False

    # ¬Q: The inverse operator T^{-1} is NOT self-adjoint with respect to B
    # This means (T^{-1})^* != T^{-1}, which is equivalent to (T^{-1})^T B != B T^{-1}.
    try:
        if h2_ok:
            T_inv = T.inv()
            neg_q_ok = bool((T_inv.transpose() * B) != (B * T_inv))
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: B is a non-degenerate bilinear form on V",
    "H_2: T is an invertible linear operator on V",
    "H_3: T is self-adjoint with respect to B (T^* = T)",
    "¬Q: The inverse operator T^{-1} is NOT self-adjoint with respect to B"
]

N_HYP = 3
NEG_Q_INDEX = 3