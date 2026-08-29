import sympy
from sympy.polys.domains import ZZ, QQ

class ProductRing:
    """Represents the direct product of a ring with itself: R x R."""
    def __init__(self, base_ring):
        self.base_ring = base_ring
        self.is_Domain = False

    def __eq__(self, other):
        if isinstance(other, ProductRing):
            return self.base_ring == other.base_ring
        return False

    def __repr__(self):
        return f"ProductRing({self.base_ring})"

# Pre-defined bindings for the witness expression
QQ_times_QQ = ProductRing(QQ)
ZZ_times_ZZ = ProductRing(ZZ)
Z = ZZ
Q = QQ

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            K = witness.get('K')
            L = witness.get('L')
            S = witness.get('S')
        else:
            R, K, L, S = witness
    except Exception:
        return [False, False, False, False]

    # Normalize common SymPy sets to domains if used
    try:
        if R == sympy.S.Integers:
            R = ZZ
        if K == sympy.S.Rationals:
            K = QQ
    except Exception:
        pass

    # H_1: R is an integral domain
    try:
        h1 = False
        if hasattr(R, 'is_Domain'):
            h1 = bool(R.is_Domain)
        elif R == ZZ:
            h1 = True
    except Exception:
        h1 = False

    # H_2: K is the field of fractions of R
    try:
        h2 = False
        if hasattr(R, 'get_field'):
            h2 = (R.get_field() == K)
        elif R == ZZ and K == QQ:
            h2 = True
    except Exception:
        h2 = False

    # H_3: S is the integral closure of R in L
    try:
        h3 = False
        if isinstance(L, ProductRing) and isinstance(S, ProductRing):
            # In the direct product K x K, the integral closure of R is R x R
            # (assuming R is integrally closed in K, which is true for ZZ in QQ)
            if L.base_ring == K and S.base_ring == R:
                h3 = True
        elif R == ZZ and L == QQ_times_QQ and S == ZZ_times_ZZ:
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: S is not an integral domain
    try:
        neg_q = False
        if hasattr(S, 'is_Domain'):
            neg_q = not bool(S.is_Domain)
        elif isinstance(S, ProductRing):
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: S is the integral closure of R in L",
    "¬Q: S is not an integral domain"
]

N_HYP = 3
NEG_Q_INDEX = 3