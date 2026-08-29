import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
Z_x = ZZ[x]
Q_x_y = QQ[x, y]

def conditions(witness):
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
    
    # H1: S is a multiplicatively closed subset of R
    try:
        h1 = True
        S_list = list(S)
        if not S_list:
            # Empty set is vacuously multiplicatively closed
            pass
        else:
            for a in S_list:
                for b in S_list:
                    if (a * b) not in S_list:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: 0 is not an element of S
    try:
        h2 = True
        S_list = list(S)
        if 0 in S_list:
            h2 = False
        if hasattr(R, 'zero') and R.zero in S_list:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: S^{-1}R is not a Euclidean domain
    try:
        neg_q = False
        S_set = set(S)
        # If S is just {1}, the localization S^{-1}R is isomorphic to R.
        if S_set == {1} or (hasattr(R, 'one') and S_set == {R.one}):
            # A Euclidean domain must be a Principal Ideal Domain (PID).
            # If R is not a PID, it cannot be a Euclidean domain.
            if hasattr(R, 'is_PID') and R.is_PID is False:
                neg_q = True
            # Also, if R is not an integral domain, it's not a Euclidean domain.
            elif hasattr(R, 'is_Domain') and R.is_Domain is False:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: 0 is not an element of S",
    "¬Q: The localization S^{-1}R is not a Euclidean domain"
]

N_HYP = 2
NEG_Q_INDEX = 2