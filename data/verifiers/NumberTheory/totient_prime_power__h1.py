import sympy
from sympy.ntheory import totient

def conditions(witness):
    try:
        p, k = witness
    except Exception:
        return [False, False]

    try:
        k_val = int(k)
        h1 = (k_val == k) and (k_val > 0) and isinstance(k, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        p_val = int(p)
        k_val = int(k)
        if p_val != p or k_val != k or not isinstance(p, (int, sympy.Integer)) or not isinstance(k, (int, sympy.Integer)):
            neg_q = False
        elif abs(p_val) > 10000 or k_val > 100:
            neg_q = False
        else:
            pk = p_val ** k_val
            pk_minus_1 = p_val ** (k_val - 1)
            lhs = totient(pk)
            rhs = pk - pk_minus_1
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: phi(p^k) != p^k - p^{k-1}"
]

N_HYP = 1
NEG_Q_INDEX = 1