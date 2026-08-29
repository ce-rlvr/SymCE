import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup: named object bindings
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, A, B = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    def is_ucc(group, subset):
        try:
            subset_set = set(subset)
        except TypeError:
            return False
        for x in subset_set:
            if not group.contains(x):
                return False
            for g in group.generators:
                if g * x * ~g not in subset_set:
                    return False
                if ~g * x * g not in subset_set:
                    return False
        return True

    # H_2: A and B are each a union of conjugacy classes of G
    try:
        h2 = is_ucc(G, A) and is_ucc(G, B)
    except Exception:
        h2 = False
        
    # ¬Q: AB is NOT a union of conjugacy classes of G
    try:
        AB = {a * b for a in A for b in B}
        neg_q = not is_ucc(G, AB)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: A and B are each a union of conjugacy classes of G",
    "¬Q: AB is not a union of conjugacy classes of G"
]

N_HYP = 2
NEG_Q_INDEX = 2