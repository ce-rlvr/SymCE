import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # ¬Q: Aut(G) does NOT contain a non-trivial element
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            # A group has a trivial automorphism group if and only if its order is 1 or 2.
            # Therefore, Aut(G) does NOT contain a non-trivial element iff order <= 2.
            neg_q_ok = bool(witness.order() <= 2)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: Aut(G) does not contain a non-trivial element"
]

N_HYP = 1
NEG_Q_INDEX = 1