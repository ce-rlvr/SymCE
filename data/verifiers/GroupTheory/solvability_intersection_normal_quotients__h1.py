import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]

    def is_subset(supergroup, subgroup):
        try:
            for g in subgroup.generators:
                if g not in supergroup:
                    return False
            return True
        except Exception:
            return False

    def is_normal_subgroup(G, H):
        try:
            if not is_subset(G, H):
                return False
            for g in G.generators:
                for h in H.generators:
                    if (g * h * ~g) not in H:
                        return False
            return True
        except Exception:
            return False

    def is_quotient_solvable(G, N):
        try:
            current = G
            while True:
                if is_subset(N, current):
                    return True
                next_group = current.derived_subgroup()
                if is_subset(current, next_group) and is_subset(next_group, current):
                    return is_subset(N, next_group)
                current = next_group
        except Exception:
            return False

    def is_intersection_quotient_solvable(G, H, K):
        try:
            current = G
            while True:
                if is_subset(H, current) and is_subset(K, current):
                    return True
                next_group = current.derived_subgroup()
                if is_subset(current, next_group) and is_subset(next_group, current):
                    return is_subset(H, next_group) and is_subset(K, next_group)
                current = next_group
        except Exception:
            return False

    try:
        h1 = is_normal_subgroup(G, H) and is_normal_subgroup(G, K)
    except Exception:
        h1 = False

    try:
        h2 = is_quotient_solvable(G, H)
    except Exception:
        h2 = False

    try:
        h3 = is_quotient_solvable(G, K)
    except Exception:
        h3 = False

    try:
        q = is_intersection_quotient_solvable(G, H, K)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H and K are normal subgroups of G",
    "H_2: The quotient group G/H is solvable",
    "H_3: The quotient group G/K is solvable",
    "¬Q: The quotient group G/(H \\cap K) is not solvable"
]

N_HYP = 3
NEG_Q_INDEX = 3