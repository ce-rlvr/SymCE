import sympy
from sympy.ntheory import totient
import math

def conditions(witness):
    try:
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            h1 = int(witness) > 0
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool) and int(witness) > 0:
            n = int(witness)
            lhs = sum(totient(k) * (n // k) for k in range(1, n + 1))
            rhs = n * (n + 1) // 2
            neg_q = bool(lhs != rhs)
        else:
            n_float = float(witness)
            upper = math.floor(n_float)
            if upper < 1:
                lhs = 0
            else:
                lhs = sum(totient(k) * math.floor(n_float / k) for k in range(1, upper + 1))
            rhs = n_float * (n_float + 1) / 2.0
            neg_q = not math.isclose(lhs, rhs, rel_tol=1e-9)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: \\sum_{k=1}^n \\phi(k) \\lfloor \\frac{n}{k} \\rfloor \\neq \\frac{n(n+1)}{2}"
]

N_HYP = 1
NEG_Q_INDEX = 1