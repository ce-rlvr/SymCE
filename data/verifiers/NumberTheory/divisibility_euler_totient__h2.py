import sympy
import sympy.ntheory

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer))
              and a > 0 and b > 0)
    except Exception:
        h1 = False

    try:
        phi_a = sympy.ntheory.totient(a)
        phi_b = sympy.ntheory.totient(b)
        neg_q = (phi_b % phi_a != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are positive integers",
    "¬Q: phi(a) does not divide phi(b)"
]

N_HYP = 1
NEG_Q_INDEX = 1