import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup

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
    # The witness should provide both groups G and H.
    # It can be a tuple/list (G, H) or a dictionary {'G': G, 'H': H}.
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
        else:
            G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is a locally nilpotent group
    # For finite groups, locally nilpotent is equivalent to nilpotent.
    try:
        h1_ok = bool(G.is_nilpotent)
    except Exception:
        h1_ok = False

    # ¬Q: The direct product G x H is NOT a locally nilpotent group
    # For finite groups, G x H is nilpotent if and only if both G and H are nilpotent.
    try:
        neg_q_ok = not (G.is_nilpotent and H.is_nilpotent)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a locally nilpotent group",
    "¬Q: The direct product G x H is not a locally nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1