import sympy
from sympy import Integer

def conditions(witness):
    try:
        x, y, z = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(x, (int, Integer)) and 
              isinstance(y, (int, Integer)) and 
              isinstance(z, (int, Integer)) and 
              x > 0 and y > 0 and z > 0)
    except Exception:
        h1 = False

    try:
        neg_q = (x**4 - (x**2)*(y**2) + y**4 == z**2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x, y, z in Z_{>0}",
    "¬Q: x^4 - x^2 y^2 + y^4 = z^2"
]

N_HYP = 1
NEG_Q_INDEX = 1