import sympy
from sympy.ntheory import totient

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness['p']
            k = witness['k']
        else:
            p, k = witness
        h1 = isinstance(k, (int, sympy.Integer)) and k > 0 and isinstance(p, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            p = witness['p']
            k = witness['k']
        else:
            p, k = witness
        lhs = totient(p**k)
        rhs = p**k - p**(k-1)
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