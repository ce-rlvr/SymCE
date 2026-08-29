import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # Extract G and H from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a solvable group
    try:
        h2 = h1 and G.is_solvable is True
    except Exception:
        h2 = False

    # neg_Q: H is not a solvable group
    try:
        is_group = isinstance(H, PermutationGroup)
        is_solvable = is_group and H.is_solvable is True
        neg_q = not is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is a solvable group",
    "¬Q: H is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2