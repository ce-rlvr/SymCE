import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, H), checks if it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: H is a locally nilpotent group
    # For finite groups, locally nilpotent is equivalent to nilpotent.
    try:
        h1_ok = bool(H.is_nilpotent)
    except Exception:
        h1_ok = False

    # ¬Q: G x H is NOT a locally nilpotent group
    # G x H is nilpotent if and only if both G and H are nilpotent.
    try:
        neg_q_ok = not (bool(G.is_nilpotent) and bool(H.is_nilpotent))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a locally nilpotent group",
    "¬Q: G x H is not a locally nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1
