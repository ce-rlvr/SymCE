import sympy
from sympy import QQ, ZZ, RR, CC

# Top-level setup
# We allow integers to represent the rings Z/nZ.
# QQ, ZZ, RR, CC are imported from sympy to represent standard rings/fields.

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample.
    The witness should be a tuple (R1, R2) representing the rings R_1 and R_2.
    Integers n represent the ring Z/nZ.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        R1, R2 = witness
    except Exception:
        return [False, False]

    def is_nonzero_comm_ring(R):
        if R in (QQ, ZZ, RR, CC):
            return True
        try:
            n = abs(int(R))
            return n != 1
        except Exception:
            return False

    def num_max_ideals(R):
        if R in (QQ, RR, CC):
            return 1
        if R == ZZ:
            return float('inf')
        try:
            n = abs(int(R))
            if n == 1:
                return 0
            if n == 0:
                return float('inf')
            return len(sympy.primefactors(n))
        except Exception:
            return float('nan')

    try:
        # H_1: R_1 is a non-zero commutative ring
        h1 = is_nonzero_comm_ring(R1)
    except Exception:
        h1 = False

    try:
        # ¬Q: The direct product ring R_1 x R_2 IS a local ring.
        # A commutative ring is local iff it has exactly one maximal ideal.
        # The maximal ideals of R_1 x R_2 are of the form M x R_2 or R_1 x M',
        # so the number of maximal ideals is the sum of those in R_1 and R_2.
        neg_q = (num_max_ideals(R1) + num_max_ideals(R2) == 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R_1 is a non-zero commutative ring",
    "¬Q: The direct product ring R_1 x R_2 is a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1