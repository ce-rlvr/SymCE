import math

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy does not have a comprehensive module for abstract local rings and their 
# homological invariants, we provide a helper class to represent Noetherian local rings 
# via their Krull dimension, depth, and injective dimension.

class NoetherianLocalRing:
    """
    Represents a Noetherian local ring by its homological invariants.
    """
    def __init__(self, krull_dim, depth, inj_dim, socle_dim=None, is_comm=True, is_loc=True):
        self.krull_dim = krull_dim
        self.depth = depth
        self.inj_dim = inj_dim
        self._socle_dim = socle_dim
        self.is_comm = is_comm
        self.is_loc = is_loc

    def is_commutative(self):
        return self.is_comm

    def is_local(self):
        return self.is_loc

    def is_gorenstein(self):
        # A local ring is Gorenstein iff it has finite injective dimension.
        # This implies it is Cohen-Macaulay (krull_dim == depth).
        return self.inj_dim < float('inf') and self.krull_dim == self.depth

    def socle_dimension(self):
        # The socle is the annihilator of the maximal ideal.
        # If depth > 0, the maximal ideal contains a regular element, so its annihilator is 0.
        if self.depth > 0:
            return 0
        # If depth == 0 and the ring is Gorenstein, it must be Artinian (krull_dim == 0).
        # An Artinian local ring is Gorenstein iff its socle is 1-dimensional.
        if self.is_gorenstein() and self.krull_dim == 0:
            return 1
        # Otherwise, return the explicitly provided socle dimension or a default > 1.
        if self._socle_dim is not None:
            return self._socle_dim
        return 2

# Predefined ring examples
Z_p = NoetherianLocalRing(krull_dim=1, depth=1, inj_dim=1) # Z localized at p (Counterexample)
k_x = NoetherianLocalRing(krull_dim=1, depth=1, inj_dim=1) # k[[x]] (Counterexample)
k_x_x2 = NoetherianLocalRing(krull_dim=0, depth=0, inj_dim=0) # k[x]/(x^2) (Artinian Gorenstein, not a counterexample)
k_x_y_x2_xy_y2 = NoetherianLocalRing(krull_dim=0, depth=0, inj_dim=float('inf'), socle_dim=2) # Artinian non-Gorenstein


def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Returns a list of booleans: [H_1, H_2, H_3, neg_Q]
    """
    # H_1: R is a commutative ring
    try:
        if callable(getattr(witness, 'is_commutative', None)):
            h1 = bool(witness.is_commutative())
        else:
            h1 = bool(witness.is_commutative)
    except Exception:
        h1 = False

    # H_2: R is a local ring with maximal ideal m and residue field k = R/m
    try:
        if callable(getattr(witness, 'is_local', None)):
            h2 = bool(witness.is_local())
        else:
            h2 = bool(witness.is_local)
    except Exception:
        h2 = False

    # H_3: R is a Gorenstein ring
    try:
        if callable(getattr(witness, 'is_gorenstein', None)):
            h3 = bool(witness.is_gorenstein())
        else:
            h3 = bool(witness.is_gorenstein)
    except Exception:
        h3 = False

    # ¬Q: The socle of R is NOT a one-dimensional vector space over k
    try:
        if callable(getattr(witness, 'socle_dimension', None)):
            socle_dim = witness.socle_dimension()
        else:
            socle_dim = witness.socle_dimension
        neg_q = bool(socle_dim != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]


CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring with maximal ideal m and residue field k = R/m",
    "H_3: R is a Gorenstein ring",
    "¬Q: The socle of R is not a one-dimensional vector space over k"
]

N_HYP = 3
NEG_Q_INDEX = 3