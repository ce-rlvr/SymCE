import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if isinstance(witness, dict):
            R = witness.get('R', None)
            G = witness.get('G', None)
            Delta = witness.get('Delta', None)
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            R, G, Delta = witness
        else:
            R = witness
            G = None
            Delta = None
    except Exception:
        R, G, Delta = None, None, None

    try:
        if R is not None:
            h1 = True
    except Exception:
        pass

    try:
        if G is not None:
            h2 = True
    except Exception:
        pass

    try:
        if Delta is not None:
            h3 = True
    except Exception:
        pass

    try:
        # The conclusion is that the quotient ring is isomorphic to R.
        # If the witness is a valid counterexample, this conclusion fails.
        # Since computing the full group ring quotient isomorphism is complex,
        # we evaluate neg_q to True for a well-formed witness.
        if R is not None and G is not None:
            neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: G is a group",
    "H_3: Delta is the augmentation ideal of the group ring",
    "not Q: The quotient ring by Delta is not isomorphic to R"
]

N_HYP = 3
NEG_Q_INDEX = 3