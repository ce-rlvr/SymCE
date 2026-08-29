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
        G, N, S = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        is_subgroup = all(g in G for g in N.generators)
        
        is_normal = True
        if is_subgroup:
            for n in N.generators:
                for g in G.generators:
                    if (g * n * ~g) not in N:
                        is_normal = False
                        break
                if not is_normal:
                    break
        else:
            is_normal = False
        
        is_semisimple = True
        if is_subgroup and is_normal:
            for H in N.normal_subgroups():
                if H.is_abelian and H.order() > 1:
                    is_semisimple = False
                    break
        else:
            is_semisimple = False
            
        h2 = is_subgroup and is_normal and is_semisimple
    except Exception:
        h2 = False

    try:
        n_elems = set(N.generate())
        s_elems = set(S.generate())
        intersection = n_elems.intersection(s_elems)
        neg_q = len(intersection) > 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal semisimple subgroup of G",
    "¬Q: The intersection of N and S is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2