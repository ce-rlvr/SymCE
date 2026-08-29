import math

class ValuationRingIdeal:
    """
    Represents an ideal in a valuation ring with value group Q (e.g., Puiseux series).
    The ideal is defined by the infimum of the valuations of its elements (>= 0),
    and whether the infimum is included in the value set.
    
    The ring R itself is represented by ValuationRingIdeal(0, True).
    The zero ideal is represented by ValuationRingIdeal(math.inf, True).
    """
    def __init__(self, infimum, closed):
        self.infimum = float(infimum)
        self.closed = bool(closed)

    def __eq__(self, other):
        if type(other) is not ValuationRingIdeal:
            return False
        if self.infimum == math.inf and other.infimum == math.inf:
            return True
        return self.infimum == other.infimum and self.closed == other.closed

    def __mul__(self, other):
        if type(other) is not ValuationRingIdeal:
            return NotImplemented
        return ValuationRingIdeal(
            self.infimum + other.infimum,
            self.closed and other.closed
        )
        
    def is_subset(self, other):
        if type(other) is not ValuationRingIdeal:
            return False
        if self.infimum == math.inf and other.infimum == math.inf:
            return True
        if self.infimum > other.infimum:
            return True
        if self.infimum == other.infimum:
            if other.closed:
                return True
            else:
                return not self.closed
        return False

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (R, J, I), verifies if it is a valid counterexample.
    """
    try:
        R, J, I = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = type(R) is ValuationRingIdeal and R == ValuationRingIdeal(0, True)
    except Exception:
        h1 = False

    # H_2: J is an ideal of R
    try:
        h2 = type(J) is ValuationRingIdeal and J.is_subset(R)
    except Exception:
        h2 = False

    # H_3: J is contained in the Jacobson radical of R
    try:
        # The Jacobson radical of this local valuation ring is its unique maximal ideal (0, False)
        jacobson = ValuationRingIdeal(0, False)
        h3 = type(J) is ValuationRingIdeal and J.is_subset(jacobson)
    except Exception:
        h3 = False

    # H_4: I = IJ
    try:
        h4 = type(I) is ValuationRingIdeal and type(J) is ValuationRingIdeal and (I == I * J)
    except Exception:
        h4 = False

    # ¬Q: I != {0}
    try:
        zero_ideal = ValuationRingIdeal(math.inf, True)
        neg_q = type(I) is ValuationRingIdeal and not (I == zero_ideal)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "H_3: J is contained in the Jacobson radical of R",
    "H_4: I = IJ",
    "¬Q: I != {0}"
]

N_HYP = 4
NEG_Q_INDEX = 4