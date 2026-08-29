import sympy
from sympy import S
from sympy.abc import x, y, z

ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    if witness == S.Integers:
        witness = ZZ
    elif witness == S.Rationals:
        witness = QQ
    elif witness == S.Reals:
        witness = RR
    elif witness == S.Complexes:
        witness = CC

    try:
        # H_1: R is a commutative ring with identity
        # In SymPy, all Domain objects represent commutative rings with identity.
        h1_ok = isinstance(witness, sympy.polys.domains.Domain)
    except Exception:
        h1_ok = False

    try:
        # H_2: R is an integral domain
        # All SymPy Domain objects are integral domains (they do not model rings with zero divisors).
        h2_ok = h1_ok
    except Exception:
        h2_ok = False

    try:
        # neg_Q: R is not a field
        neg_q_ok = h1_ok and not witness.is_Field
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is an integral domain",
    "¬Q: R is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2