import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, N_list = witness
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: I is a non-empty index set (N_i are subgroups of G)
    try:
        h2 = False
        if isinstance(N_list, (list, tuple, set)) and len(N_list) > 0:
            all_subgroups = True
            for N in N_list:
                if not isinstance(N, PermutationGroup):
                    all_subgroups = False
                    break
                # Check if N is a subgroup of G by verifying its generators are in G
                for gen in N.generators:
                    if gen not in G:
                        all_subgroups = False
                        break
                if not all_subgroups:
                    break
            h2 = all_subgroups
    except Exception:
        h2 = False

    # neg_Q: The intersection of all N_i is NOT a normal subgroup of G
    try:
        neg_q = False
        if h1 and h2:
            G_elems = list(G.generate())
            
            # Compute the intersection of all subgroups N_i
            intersect_elems = set()
            for g in G_elems:
                in_all = True
                for N in N_list:
                    if g not in N:
                        in_all = False
                        break
                if in_all:
                    intersect_elems.add(g)
            
            # Check if the intersection forms a normal subgroup
            is_normal = True
            for g in G_elems:
                for h in intersect_elems:
                    conj = g * h * (~g)
                    if conj not in intersect_elems:
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: I is a non-empty index set (N_i are subgroups of G)",
    "¬Q: The intersection of all N_i is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2