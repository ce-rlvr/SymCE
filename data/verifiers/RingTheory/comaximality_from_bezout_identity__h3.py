import sympy
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: a and b are elements of R",
    "¬Q: The principal ideals (a) and (b) are not comaximal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        a, b = witness
    except Exception:
        return [False, False, False]

    try:
        valid_types = (int, sympy.Integer, sympy.Expr)
        if not (isinstance(a, valid_types) and isinstance(b, valid_types)):
            h1 = False
        elif isinstance(a, sympy.MatrixBase) or isinstance(b, sympy.MatrixBase):
            h1 = False
        elif hasattr(a, 'is_commutative') and a.is_commutative is False:
            h1 = False
        elif hasattr(b, 'is_commutative') and b.is_commutative is False:
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        g = sympy.gcd(a, b)
        if isinstance(g, (int, sympy.Integer)):
            is_unit = (abs(g) == 1)
        else:
            is_unit = (g == 1 or g == -1)
        
        neg_q = not is_unit
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]