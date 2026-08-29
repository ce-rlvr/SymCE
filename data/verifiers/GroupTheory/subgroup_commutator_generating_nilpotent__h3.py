import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a nilpotent group
    try:
        h1_ok = bool(G.is_nilpotent)
    except Exception:
        h1_ok = False

    # H_2: H is a subgroup of G
    try:
        h2_ok = bool(H.is_subgroup(G))
    except Exception:
        h2_ok = False

    # ¬Q: H != G
    try:
        # If they are both subgroups of each other, they are equal.
        # The conclusion fails if they are NOT equal.
        neg_q_ok = not (H.is_subgroup(G) and G.is_subgroup(H))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: H is a subgroup of G",
    "¬Q: H is not equal to G"
]

N_HYP = 2
NEG_Q_INDEX = 2