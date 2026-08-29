import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
        if len(witness) != 3:
            return [False, False, False, False]
        G, H, g = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if isinstance(H, PermutationGroup) and h1:
            try:
                h2 = bool(H.is_subgroup(G))
            except AttributeError:
                h2 = all(gen in G for gen in H.generators)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: g is an element of G
    try:
        h3 = isinstance(g, Permutation) and h1 and bool(g in G)
    except Exception:
        h3 = False

    # neg_Q: g^2 is NOT in H
    try:
        neg_q = h2 and h3 and bool((g**2) not in H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: g is an element of G",
    "¬Q: g^2 is not in H"
]

N_HYP = 3
NEG_Q_INDEX = 3