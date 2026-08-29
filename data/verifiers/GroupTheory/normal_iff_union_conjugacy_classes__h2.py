import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a group
    h1 = False
    try:
        if isinstance(G, PermutationGroup):
            H_set = set(H)
            h1 = True
            for h in H_set:
                if not isinstance(h, Permutation) or h not in G:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # ¬Q: H is a normal subgroup of G if and only if H can be expressed as a union of conjugacy classes of G
    neg_q = False
    try:
        if h1:
            H_set = set(H)
            
            # Check if H is a subgroup
            is_subgroup = False
            if len(H_set) > 0:
                if G.identity in H_set:
                    closed_mult = True
                    for a in H_set:
                        for b in H_set:
                            if a * b not in H_set:
                                closed_mult = False
                                break
                        if not closed_mult:
                            break
                    
                    closed_inv = True
                    if closed_mult:
                        for a in H_set:
                            if ~a not in H_set:
                                closed_inv = False
                                break
                    
                    is_subgroup = closed_mult and closed_inv

            # Check if H is a union of conjugacy classes of G
            is_union_of_cc = True
            for h in H_set:
                for g in G.generators:
                    if g * h * ~g not in H_set:
                        is_union_of_cc = False
                        break
                    if ~g * h * g not in H_set:
                        is_union_of_cc = False
                        break
                if not is_union_of_cc:
                    break
            
            is_normal_subgroup = is_subgroup and is_union_of_cc
            
            # The conjecture claims: is_normal_subgroup == is_union_of_cc
            # The negation is that they are not equivalent
            neg_q = (is_normal_subgroup != is_union_of_cc)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: H is a normal subgroup of G if and only if H can be expressed as a union of conjugacy classes of G (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1