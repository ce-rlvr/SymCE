import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        G, A, B = witness
        h1 = isinstance(G, PermutationGroup) and isinstance(A, (set, list, tuple)) and isinstance(B, (set, list, tuple))
    except Exception:
        h1 = False

    try:
        domain = set(range(G.degree))
        h2 = all(x in domain for x in A) and all(x in domain for x in B)
    except Exception:
        h2 = False

    try:
        A_set = set(A)
        B_set = set(B)
        A_union_B = A_set.union(B_set)

        def pointwise_stab(group, subset):
            stab = set()
            for g in group.elements:
                if all(g(x) == x for x in subset):
                    stab.add(g)
            return stab

        stab_A = pointwise_stab(G, A_set)
        stab_B = pointwise_stab(G, B_set)
        stab_union = pointwise_stab(G, A_union_B)

        intersection = stab_A.intersection(stab_B)

        neg_q = (stab_union != intersection)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a permutation group acting on a set X",
    "H_2: A and B are subsets of X",
    "¬Q: G_{(A U B)} != G_{(A)} intersection G_{(B)}"
]

N_HYP = 2
NEG_Q_INDEX = 2