import math
import sympy

def conditions(witness):
    """
    Given a witness (a, b, c), checks if it satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    try:
        a, b, c = witness
    except Exception:
        return [False, False]

    # H_1: a, b, and c are integers
    try:
        h1 = (isinstance(a, (int, sympy.Integer)) and 
              isinstance(b, (int, sympy.Integer)) and 
              isinstance(c, (int, sympy.Integer)))
    except Exception:
        h1 = False

    # ¬Q: gcd(ac, b) != gcd(c, b)
    try:
        a_int = int(a)
        b_int = int(b)
        c_int = int(c)
        neg_q = math.gcd(a_int * c_int, b_int) != math.gcd(c_int, b_int)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are integers",
    "¬Q: gcd(ac, b) != gcd(c, b)"
]

N_HYP = 1
NEG_Q_INDEX = 1