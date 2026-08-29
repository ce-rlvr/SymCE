import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: x is an element of R
    try:
        _ = witness + witness
        _ = witness * witness
        _ = witness - witness
        h1 = True
    except Exception:
        h1 = False

    # ¬Q: x + x != 0
    try:
        val = witness + witness
        
        def is_zero(v):
            if hasattr(v, 'is_zero_matrix'):
                return bool(v.is_zero_matrix)
            if hasattr(v, 'is_zero') and v.is_zero is not None:
                return bool(v.is_zero)
            if v == 0:
                return True
            try:
                if sympy.simplify(v) == 0:
                    return True
            except Exception:
                pass
            return False
            
        neg_q = not is_zero(val)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of R",
    "¬Q: x + x != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1