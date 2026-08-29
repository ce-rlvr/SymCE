import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is an abelian group
    try:
        h1_ok = bool(G.is_abelian)
    except Exception:
        h1_ok = False

    # ¬Q: The direct product G x H is NOT an abelian group
    # The direct product of two groups is abelian if and only if both groups are abelian.
    try:
        neg_q_ok = not (bool(G.is_abelian) and bool(H.is_abelian))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: The direct product G x H is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1