import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        G, H = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, (list, set, tuple)) and len(H) > 0 and all(h in G for h in H)
    except Exception:
        h2 = False

    try:
        h3 = isinstance(H, (list, set, tuple))
    except Exception:
        h3 = False

    try:
        if not h2:
            neg_q = False
        else:
            H_set = set(H)
            is_subgroup = True
            if G.identity not in H_set:
                is_subgroup = False
            else:
                for a in H_set:
                    if ~a not in H_set:
                        is_subgroup = False
                        break
                    for b in H_set:
                        if a * b not in H_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
            neg_q = not is_subgroup
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a non-empty subset of G",
    "H_3: H is finite",
    "¬Q: H is not a subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3