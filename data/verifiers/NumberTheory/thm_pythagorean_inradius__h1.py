import sympy
from sympy import Rational, Integer, Float

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False]
        x, y, z = witness
    except Exception:
        return [False, False]
        
    try:
        x_sym = sympy.sympify(x)
        y_sym = sympy.sympify(y)
        z_sym = sympy.sympify(z)
        diff = sympy.simplify(x_sym**2 + y_sym**2 - z_sym**2)
        if diff == 0:
            h1 = True
        else:
            try:
                h1 = abs(float(diff)) < 1e-12
            except Exception:
                h1 = False
    except Exception:
        h1 = False

    try:
        x_sym = sympy.sympify(x)
        y_sym = sympy.sympify(y)
        z_sym = sympy.sympify(z)
        val = sympy.simplify((x_sym + y_sym - z_sym) / 2)
        
        if val.is_integer is not None:
            is_int = bool(val.is_integer)
        else:
            try:
                is_int = float(val).is_integer()
            except Exception:
                is_int = False
        neg_q = not is_int
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x^2 + y^2 = z^2",
    "¬Q: (x + y - z) / 2 is not an integer"
]

N_HYP = 1
NEG_Q_INDEX = 1