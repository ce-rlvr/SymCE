import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        G, M = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    try:
        h2 = bool(G.is_nilpotent)
    except Exception:
        h2 = False

    try:
        is_subgroup = all(G.contains(m) for m in M.generators)
        if not is_subgroup:
            neg_q = False
        else:
            is_normal = True
            for g in G.generators:
                for m in M.generators:
                    if not M.contains(g * m * ~g):
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a nilpotent group",
    "¬Q: M is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2