import sympy
from sympy import QQ, ZZ
from sympy.polys.domains import Domain

class InfinitePolynomialRing:
    """Representation of a polynomial ring with infinitely many variables, e.g., R[X_1, X_2, ...]"""
    def __init__(self, base_ring):
        self.base_ring = base_ring

    @property
    def is_commutative(self):
        return True

    @property
    def is_noetherian(self):
        return False

    def __eq__(self, other):
        return isinstance(other, InfinitePolynomialRing) and self.base_ring == other.base_ring

    def contains_subring(self, other):
        if self == other:
            return True
        if getattr(other, 'is_commutative', False) and other == self.base_ring:
            return True
        return False

    def is_finitely_generated_module_over(self, R):
        if self == R:
            return True
        return False

# Top-level setup: named object bindings that the witness expression may reference.
Z_inf_poly = InfinitePolynomialRing(ZZ)
Q_inf_poly = InfinitePolynomialRing(QQ)

def check_commutative(ring):
    if hasattr(ring, 'is_commutative'):
        val = ring.is_commutative
        return val() if callable(val) else val
    if isinstance(ring, Domain):
        return True
    return False

def check_noetherian(ring):
    if hasattr(ring, 'is_noetherian'):
        val = ring.is_noetherian
        return val() if callable(val) else val
    if isinstance(ring, Domain):
        return True
    return True

def check_subring(R, S):
    if R == S:
        return True
    if hasattr(S, 'contains_subring'):
        return S.contains_subring(R)
    if isinstance(R, Domain) and isinstance(S, Domain):
        try:
            return S.unify(R) == S
        except Exception:
            return False
    return False

def check_finitely_generated_module(S, R):
    if R == S:
        return True
    if hasattr(S, 'is_finitely_generated_module_over'):
        return S.is_finitely_generated_module_over(R)
    return False

def conditions(witness) -> list[bool]:
    if not isinstance(witness, tuple) or len(witness) != 2:
        return [False, False, False]
        
    R, S = witness
    
    # H_1: R and S are commutative rings such that R is a subring of S
    try:
        h1_R_comm = check_commutative(R)
        h1_S_comm = check_commutative(S)
        h1_subring = check_subring(R, S)
        h1 = bool(h1_R_comm and h1_S_comm and h1_subring)
    except Exception:
        h1 = False
        
    # H_2: S is a finitely generated module over R
    try:
        h2 = bool(check_finitely_generated_module(S, R))
    except Exception:
        h2 = False
        
    # ¬Q: R is not a Noetherian ring
    try:
        neg_q = not check_noetherian(R)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings such that R is a subring of S",
    "H_2: S is a finitely generated module over R",
    "¬Q: R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2