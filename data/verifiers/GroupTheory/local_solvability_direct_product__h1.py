import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # The witness should be a tuple of two groups: (G, H)
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    try:
        # For finite groups, local solvability is equivalent to solvability.
        h1_ok = bool(H.is_solvable)
    except Exception:
        h1_ok = False

    try:
        # The direct product G x H is solvable if and only if both G and H are solvable.
        # The conclusion Q states that G x H is locally solvable.
        # We want the negation of Q, meaning G x H is NOT locally solvable.
        neg_q_ok = not (bool(G.is_solvable) and bool(H.is_solvable))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a locally solvable group",
    "¬Q: G x H is not a locally solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1
