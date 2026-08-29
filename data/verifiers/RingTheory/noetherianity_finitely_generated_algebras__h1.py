import math

class AbstractRing:
    """A mock class to represent abstract rings with specific properties."""
    def __init__(self, commutative=True, noetherian=True):
        self.commutative = bool(commutative)
        self.noetherian = bool(noetherian)

    def is_commutative(self):
        return self.commutative

    def is_noetherian(self):
        return self.noetherian

class RAlgebra:
    """A mock class to represent an algebra over a base ring."""
    def __init__(self, base_ring, num_gens):
        self.base_ring = base_ring
        self.num_gens = float(num_gens)

    def is_commutative(self):
        return self.base_ring.is_commutative()

    def is_finitely_generated_over_R(self):
        return self.num_gens < float('inf')

    def is_noetherian(self):
        if self.num_gens == float('inf'):
            return False
        return self.base_ring.is_noetherian()

# Predefined objects for witness construction
NonNoetherianRing = AbstractRing(commutative=True, noetherian=False)
Z = AbstractRing(commutative=True, noetherian=True)
Q = AbstractRing(commutative=True, noetherian=True)

def conditions(witness) -> list[bool]:
    # Allow witness to be either the algebra A itself, or a tuple (R, A)
    if isinstance(witness, tuple) and len(witness) == 2:
        A = witness[1]
    else:
        A = witness

    try:
        h1 = isinstance(A, RAlgebra) and bool(A.is_commutative())
    except Exception:
        h1 = False

    try:
        h2 = isinstance(A, RAlgebra) and bool(A.is_finitely_generated_over_R())
    except Exception:
        h2 = False

    try:
        neg_q = isinstance(A, RAlgebra) and not bool(A.is_noetherian())
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a commutative R-algebra",
    "H_2: A is finitely generated as an algebra over R",
    "¬Q: A is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2