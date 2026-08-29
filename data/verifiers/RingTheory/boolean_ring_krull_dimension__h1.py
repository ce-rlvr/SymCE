import sympy
from sympy import ZZ, QQ, FF
from sympy.abc import x, y, z

ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)
ZZ_x_y = ZZ.poly_ring(x, y)
QQ_x_y = QQ.poly_ring(x, y)

def get_krull_dim(R):
    if getattr(R, 'is_Field', False):
        return 0
    if R == ZZ or R.__class__.__name__ == 'IntegerRing':
        return 1
    if getattr(R, 'is_PolynomialRing', False):
        return get_krull_dim(R.domain) + len(R.gens)
    if getattr(R, 'is_FractionField', False):
        return 0
    raise ValueError("Cannot determine Krull dimension for this domain")

def conditions(witness):
    try:
        h1 = hasattr(witness, 'one') and witness.one is not None
    except Exception:
        h1 = False

    try:
        h2 = hasattr(witness, 'zero') and hasattr(witness, 'one') and witness.zero != witness.one
    except Exception:
        h2 = False

    try:
        dim = get_krull_dim(witness)
        neg_q = (dim != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity 1",
    "H_2: R is non-trivial (1 != 0)",
    "¬Q: The Krull dimension of R is not 0"
]

N_HYP = 2
NEG_Q_INDEX = 2