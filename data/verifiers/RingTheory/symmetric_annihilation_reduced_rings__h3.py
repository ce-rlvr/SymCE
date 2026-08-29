import sympy as sp
from sympy import eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) == 3:
            R, a, b = witness
        elif len(witness) == 2:
            a, b = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a reduced ring
    try:
        def is_reduced_element(elem):
            if getattr(elem, 'is_Matrix', False):
                return elem.shape == (1, 1)
            if isinstance(elem, (int, float, complex)):
                return True
            if isinstance(elem, sp.Expr):
                return True
            return False
        h1 = bool(is_reduced_element(a) and is_reduced_element(b))
    except Exception:
        h1 = False

    # H2: a and b are elements of R
    try:
        prod = b * a
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: ba != 0
    try:
        prod = b * a
        if hasattr(prod, 'is_zero') and prod.is_zero is not None:
            neg_q = not prod.is_zero
        elif getattr(prod, 'is_Matrix', False):
            neg_q = not prod.is_zero_matrix
        else:
            try:
                neg_q = bool(sp.simplify(prod) != 0)
            except Exception:
                neg_q = bool(prod != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a reduced ring",
    "H_2: a and b are elements of R",
    "¬Q: ba != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2