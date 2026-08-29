import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G) and H.is_normal(G)
    except Exception:
        h2 = False

    try:
        h3 = isinstance(K, PermutationGroup) and K.is_subgroup(G) and K.is_normal(G)
    except Exception:
        h3 = False

    try:
        h4 = bool(H.is_solvable)
    except Exception:
        h4 = False

    try:
        if isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup):
            gens = list(H.generators) + list(K.generators)
            HK = PermutationGroup(gens)
            q = HK.is_subgroup(G) and HK.is_normal(G) and HK.is_solvable
            neg_q = not bool(q)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a normal subgroup of G",
    "H_3: K is a normal subgroup of G",
    "H_4: H is a solvable group",
    "¬Q: HK is not a normal solvable subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4