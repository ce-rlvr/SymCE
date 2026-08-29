import sympy

# Top-level setup
class PowerSetRing:
    """
    Represents the Boolean ring of all subsets of a set of given cardinality.
    Valid cardinalities: 'finite', 'aleph_0', 'aleph_1', 'aleph_2', 'uncountable'
    """
    def __init__(self, cardinality='aleph_1'):
        self.cardinality = str(cardinality)

    def is_Boolean_ring(self):
        return True

    def has_identity(self):
        return True

def _is_infinite_cardinal(c):
    return c in ['aleph_0', 'aleph_1', 'aleph_2', 'uncountable']

def _cardinal_less_than(c1, c2):
    order = {'finite': 0, 'aleph_0': 1, 'aleph_1': 2, 'aleph_2': 3, 'uncountable': 4, 'all': 5}
    return order.get(c1, -1) < order.get(c2, -1)

class CardinalityBoundedIdeal:
    """
    Represents the ideal of subsets of cardinality <= max_cardinality.
    """
    def __init__(self, ring, max_cardinality='aleph_0'):
        self.ring = ring
        self.max_cardinality = str(max_cardinality)

    def is_ideal(self):
        valid = ['finite', 'aleph_0', 'aleph_1', 'aleph_2', 'uncountable', 'all']
        return self.max_cardinality in valid

    def is_projective_module(self):
        # In a Boolean ring, an ideal is projective iff it is a direct sum of principal ideals.
        if self.max_cardinality == 'finite':
            # The ideal of finite subsets is a direct sum of singletons (which are principal).
            return True
        if self.max_cardinality == 'all' or self.max_cardinality == self.ring.cardinality:
            # The whole ring is a principal ideal, hence projective.
            return True
        
        if _is_infinite_cardinal(self.max_cardinality):
            if _cardinal_less_than(self.max_cardinality, self.ring.cardinality):
                # The ideal of subsets of size <= kappa in a set of size lambda > kappa
                # cannot be a direct sum of principal ideals.
                return False
            if self.max_cardinality == self.ring.cardinality:
                return True
                
        return True

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            R = witness.R
            I = witness.I
    except Exception:
        return [False, False]

    # H_1: R is a Boolean ring with identity and I is an ideal of R
    try:
        h1 = bool(R.is_Boolean_ring() and R.has_identity() and I.is_ideal())
    except Exception:
        h1 = False

    # ¬Q: I is not a projective R-module
    try:
        try:
            proj = I.is_projective_module()
        except TypeError:
            proj = I.is_projective_module(R)
        neg_q = not bool(proj)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring with identity and I is an ideal of R",
    "¬Q: I is not a projective R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1