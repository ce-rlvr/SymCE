import sympy
from sympy import isprime, jacobi_symbol

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        p, a = witness
    except Exception:
        return [False, False, False]

    # H_1: p is an odd prime
    try:
        h1 = bool(isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    # H_2: a is an integer
    try:
        h2 = bool(isinstance(a, (int, sympy.Integer)))
    except Exception:
        h2 = False

    # neg_Q: sum_{x=0}^{p-1} (x(x+a)/p) != -1
    try:
        if h1 and h2:
            if p > 100000:
                neg_q = False
            else:
                s = sum(jacobi_symbol(x * (x + a), p) for x in range(p))
                neg_q = bool(s != -1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: a is an integer",
    "¬Q: sum_{x=0}^{p-1} (x(x+a)/p) != -1"
]

N_HYP = 2
NEG_Q_INDEX = 2