import sympy
from sympy import ZZ, QQ, S
from sympy.abc import x, y, z
import sympy.polys.domains

def normalize_ring(R):
    """Convert common sympy Sets to their corresponding polys Domains."""
    if R == S.Integers:
        return ZZ
    if R == S.Rationals:
        return QQ
    if R == S.Reals:
        from sympy import RR
        return RR
    if R == S.Complexes:
        from sympy import CC
        return CC
    return R

def get_krull_dimension(R):
    """
    Computes the Krull dimension for standard sympy domains.
    Fields have dimension 0.
    ZZ has dimension 1.
    Polynomial rings R[x1, ..., xn] have dimension dim(R) + n.
    """
    if getattr(R, 'is_Field', False):
        return 0
    if R == ZZ:
        return 1
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        return get_krull_dimension(R.domain) + len(R.symbols)
    raise ValueError("Cannot compute Krull dimension for this domain")

def conditions(witness) -> list[bool]:
    witness = normalize_ring(witness)
    
    # H_1: R is a commutative ring
    # In sympy, all polys.domains.Domain instances are commutative rings.
    try:
        h1 = isinstance(witness, sympy.polys.domains.Domain)
    except Exception:
        h1 = False

    # H_2: R has a multiplicative identity
    try:
        h2 = isinstance(witness, sympy.polys.domains.Domain) and hasattr(witness, 'one') and witness.one is not None
    except Exception:
        h2 = False

    # ¬Q: The Krull dimension of R is not zero
    try:
        dim = get_krull_dimension(witness)
        neg_q = (dim != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "¬Q: The Krull dimension of R is not zero"
]

N_HYP = 2
NEG_Q_INDEX = 2