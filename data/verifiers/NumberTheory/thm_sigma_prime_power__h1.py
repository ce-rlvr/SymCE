import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness['p']
            k = witness['k']
        else:
            p, k = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(k, int) or isinstance(k, sympy.Integer)) and k > 0
    except Exception:
        h1 = False

    try:
        if not (isinstance(p, int) or isinstance(p, sympy.Integer)):
            neg_q = False
        elif p == 1:
            neg_q = False
        else:
            lhs = divisor_sigma(p**k)
            rhs = (p**(k+1) - 1) // (p - 1)
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: sigma(p^k) != (p^{k+1}-1)/(p-1)"
]

N_HYP = 1
NEG_Q_INDEX = 1