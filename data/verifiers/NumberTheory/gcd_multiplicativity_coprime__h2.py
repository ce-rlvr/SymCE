import sympy
import math

# Top-level setup
# No specific named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(a, (int, sympy.Integer)) and 
              isinstance(b, (int, sympy.Integer)) and 
              isinstance(c, (int, sympy.Integer)) and 
              a != 0 and b != 0 and c != 0)
    except Exception:
        h1 = False

    try:
        a_int, b_int, c_int = int(a), int(b), int(c)
        neg_q = math.gcd(a_int * b_int, c_int) != math.gcd(a_int, c_int) * math.gcd(b_int, c_int)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are non-zero integers",
    "¬Q: gcd(ab, c) != gcd(a, c) gcd(b, c)"
]

N_HYP = 1
NEG_Q_INDEX = 1