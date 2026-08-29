import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            try:
                h2 = bool(N.is_subgroup(G) and N.is_normal(G))
            except AttributeError:
                elements_G = set(G.generate())
                is_sub = all(n in elements_G for n in N.generators)
                if not is_sub:
                    h2 = False
                else:
                    elements_N = set(N.generate())
                    is_normal = True
                    for g in G.generators:
                        for n in N.generators:
                            if g * n * ~g not in elements_N:
                                is_normal = False
                                break
                        if not is_normal:
                            break
                    h2 = is_normal
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            h3 = False
        else:
            h3 = (G.order() % N.order() == 0)
    except Exception:
        h3 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            try:
                H_int_N = H.intersect(N)
                int_order = H_int_N.order()
            except Exception:
                elements_N = set(N.generate())
                int_order = sum(1 for h in H.generate() if h in elements_N)
            
            if int_order == 0:
                neg_q = False
            else:
                index_H = H.order() / int_order
                index_G = G.order() / N.order()
                neg_q = bool(index_H > index_G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: The index of N in G is finite",
    "¬Q: The index of H intersection N in H is not finite or is greater than the index of N in G"
]

N_HYP = 3
NEG_Q_INDEX = 3