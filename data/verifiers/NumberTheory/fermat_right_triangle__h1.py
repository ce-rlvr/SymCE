import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        x, y, z = witness
        x_sym = sympy.sympify(x)
        y_sym = sympy.sympify(y)
        z_sym = sympy.sympify(z)
        
        def is_zero(val):
            if val == 0:
                return True
            if hasattr(val, 'is_zero') and val.is_zero is True:
                return True
            try:
                if abs(complex(val)) < 1e-12:
                    return True
            except Exception:
                pass
            return False

        if is_zero(x_sym) or is_zero(y_sym) or is_zero(z_sym):
            neg_q = False
        else:
            diff = sympy.simplify(x_sym**4 + y_sym**4 - z_sym**2)
            if is_zero(diff):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: x^4 + y^4 = z^2 has a solution with x, y, z all non-zero"
]

N_HYP = 0
NEG_Q_INDEX = 0