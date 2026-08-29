import sympy
from sympy.abc import x

# Top-level setup: named object bindings
ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

try:
    ZZ_x = ZZ.poly_ring(x)
    QQ_x = QQ.poly_ring(x)
except Exception:
    ZZ_x = None
    QQ_x = None

def conditions(witness) -> list[bool]:
    # Shortcuts for common SymPy sets that represent standard rings/fields
    try:
        if witness == sympy.S.Integers:
            return [True, True, True, True]
        if witness in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            return [True, True, True, False]
    except Exception:
        pass

    # H_1: R is a commutative ring
    try:
        # In SymPy, Domain objects represent commutative rings
        h1 = getattr(witness, 'is_Ring', False) or getattr(witness, 'is_Field', False)
    except Exception:
        h1 = False

    # H_2: R has a multiplicative identity
    try:
        h2 = hasattr(witness, 'one') and witness.one is not None
    except Exception:
        h2 = False

    # H_3: R is an integral domain
    try:
        h3 = False
        if h1:
            # SymPy domains that are integral domains typically have a fraction field
            if hasattr(witness, 'get_field') or hasattr(witness, 'frac_field'):
                h3 = True
            # Fallback for known integral domains
            elif witness in (ZZ, QQ, RR, CC, ZZ_x, QQ_x) and witness is not None:
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: R is not a field
    try:
        neg_q = not getattr(witness, 'is_Field', False)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "H_3: R is an integral domain",
    "¬Q: R is not a field"
]

N_HYP = 3
NEG_Q_INDEX = 3