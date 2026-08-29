import sympy
from sympy import ZZ, QQ, Symbol

# Top-level setup
x = Symbol('x')
try:
    Zx = ZZ.poly_ring(x)
except Exception:
    try:
        Zx = ZZ[x]
    except Exception:
        Zx = None

def conditions(witness) -> list[bool]:
    # H_1: R is finitely generated as a ring
    try:
        def is_fg(R):
            if R == ZZ:
                return True
            if hasattr(R, 'is_FiniteField') and R.is_FiniteField:
                return True
            if hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
                return is_fg(R.domain)
            if R.__class__.__name__ == 'IntegerModRing':
                return True
            return False
        h1 = bool(is_fg(witness))
    except Exception:
        h1 = False

    # ¬Q: R is not a finite ring
    try:
        def is_fin(R):
            if hasattr(R, 'is_FiniteField') and R.is_FiniteField:
                return True
            if R.__class__.__name__ == 'IntegerModRing':
                return True
            if R == ZZ or R == QQ:
                return False
            if hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
                return False
            if hasattr(R, 'is_RationalField') and R.is_RationalField:
                return False
            if hasattr(R, 'is_RealField') and R.is_RealField:
                return False
            if hasattr(R, 'is_ComplexField') and R.is_ComplexField:
                return False
            # Default to True so that unknown rings don't accidentally pass neg_Q
            return True
        neg_q = not is_fin(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is finitely generated as a ring",
    "¬Q: R is not a finite ring"
]

N_HYP = 1
NEG_Q_INDEX = 1