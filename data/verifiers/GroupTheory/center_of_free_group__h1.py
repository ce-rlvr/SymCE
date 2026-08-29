import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy import eye, zeros

# Top-level setup: named object bindings
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
    # Extract F and S from the witness
    F = None
    S = None
    if isinstance(witness, dict):
        F = witness.get('F')
        S = witness.get('S')
    elif isinstance(witness, tuple) and len(witness) == 2:
        F, S = witness
    else:
        F = witness
        try:
            S = F.generators
        except AttributeError:
            S = []

    # H_1: The cardinality of S is greater than or equal to 2
    try:
        h1_ok = len(S) >= 2
    except Exception:
        h1_ok = False

    # ¬Q: The center of F is not the trivial subgroup
    try:
        # A group has a trivial center if its center's order is exactly 1.
        # Thus, the center is NOT trivial if the order is > 1.
        neg_q_ok = F.center().order() > 1
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The cardinality of S is greater than or equal to 2",
    "¬Q: The center of F is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1