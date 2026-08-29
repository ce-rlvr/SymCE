import sympy
from sympy import symbols, Poly

QQ = sympy.QQ
ZZ = sympy.ZZ
GF = sympy.GF

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        F = witness.get('F', QQ)
        a = witness.get('a', 0)
    elif isinstance(witness, tuple) and len(witness) == 2:
        F, a = witness
    else:
        F = QQ
        a = witness

    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    try:
        h2 = bool(F.characteristic != 2)
    except Exception:
        h2 = False

    try:
        x = symbols('x')
        poly_x = Poly(x**2 - a, x, domain=F)
        h3 = bool(poly_x.is_irreducible)
    except Exception:
        h3 = False

    try:
        x, y = symbols('x y')
        poly_xy = Poly(x**2 - a*y**2, x, y, domain=F)
        neg_q = not bool(poly_xy.is_irreducible)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The characteristic of F is not equal to 2",
    "H_3: a is not a perfect square in F",
    "neg_Q: The polynomial x^2 - a y^2 is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3