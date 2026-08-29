import sympy
from sympy import symbols, ZZ, QQ

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = symbols('x y z')
ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)
QQ_x_y = QQ.poly_ring(x, y)
ZZ_x_y = ZZ.poly_ring(x, y)

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative ring
    try:
        # In SymPy, domain objects represent commutative rings.
        h1 = hasattr(witness, 'is_PID') and hasattr(witness, 'poly_ring')
    except Exception:
        h1 = False

    # H_2: R is an integral domain
    try:
        def is_integral_domain(D):
            if getattr(D, 'is_Field', False):
                return True
            if D in (ZZ, QQ):
                return True
            if hasattr(D, 'domain') and D.domain is not D:
                return is_integral_domain(D.domain)
            return False
        
        h2 = bool(h1 and is_integral_domain(witness))
    except Exception:
        h2 = False

    # ¬Q: R is not a principal ideal domain
    try:
        neg_q = bool(h1 and not witness.is_PID)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is an integral domain",
    "¬Q: R is not a principal ideal domain"
]

N_HYP = 2
NEG_Q_INDEX = 2