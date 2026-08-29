import sympy

def conditions(witness):
    try:
        a, b, c = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(a, (int, sympy.Integer)) and 
              isinstance(b, (int, sympy.Integer)) and 
              isinstance(c, (int, sympy.Integer)) and 
              a > 0 and b > 0 and c > 0)
    except Exception:
        h1 = False

    try:
        neg_q = (a % 5 != 0) and (b % 5 != 0) and (c % 5 != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, and c are positive integers",
    "¬Q: None of a, b, or c is divisible by 5"
]

N_HYP = 1
NEG_Q_INDEX = 1