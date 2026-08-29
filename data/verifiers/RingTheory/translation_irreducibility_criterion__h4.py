import sympy
from sympy import Poly, QQ, Symbol
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        F, f, c = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = getattr(F, 'is_Field', False) or getattr(F, 'is_field', False) or F == QQ
    except Exception:
        h1 = False

    try:
        h2 = isinstance(f, Poly) and f.domain == F
    except Exception:
        h2 = False

    try:
        h3 = c in F
    except Exception:
        h3 = False

    try:
        neg_q = not f.is_irreducible
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "H_3: c is an element of F",
    "¬Q: f is not irreducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3