import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        h2_ok = False
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            if hasattr(H, 'is_subgroup'):
                h2_ok = bool(H.is_subgroup(G))
            else:
                h2_ok = all((g in G) for g in H.generators)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = False
        if isinstance(H, PermutationGroup):
            solvable = H.is_solvable
            if callable(solvable):
                solvable = solvable()
            neg_q_ok = not bool(solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: H is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2