import sympy
from sympy import Rational, Integer, sqrt

def conditions(witness):
    try:
        # Witness should be an iterable of two elements (x, y)
        x, y = witness
        x = sympy.sympify(x)
        y = sympy.sympify(y)
    except Exception:
        return [False, False]

    try:
        # H_1: x^2 + xy + y^2 = 1
        val = sympy.simplify(x**2 + x*y + y**2 - 1)
        h1_ok = bool(val == 0)
    except Exception:
        h1_ok = False

    try:
        # ¬Q: (x,y) not in {(1,0), (-1,0), (0,1), (0,-1), (1,-1), (-1,1)}
        known_solutions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
        is_known = False
        for kx, ky in known_solutions:
            if sympy.simplify(x - kx) == 0 and sympy.simplify(y - ky) == 0:
                is_known = True
                break
        neg_q_ok = not is_known
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x^2 + xy + y^2 = 1",
    "¬Q: (x,y) is not in {(1,0), (-1,0), (0,1), (0,-1), (1,-1), (-1,1)}"
]

N_HYP = 1
NEG_Q_INDEX = 1