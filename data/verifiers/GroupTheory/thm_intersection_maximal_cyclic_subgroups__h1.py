import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        F, A, B = witness
    except Exception:
        return [False, False, False]
        
    try:
        if isinstance(F, (list, tuple)):
            F = PermutationGroup(F)
        if isinstance(A, (list, tuple)):
            A = PermutationGroup(A)
        if isinstance(B, (list, tuple)):
            B = PermutationGroup(B)
    except Exception:
        pass

    # H_1: A and B are maximal cyclic subgroups of F
    try:
        def is_maximal_cyclic(group_F, group_G):
            # Check if G is a subgroup of F
            for g in group_G.generators:
                if g not in group_F:
                    return False
            
            order_G = group_G.order()
            
            # Check if G is cyclic
            is_cyclic = False
            for g in group_G.elements:
                if g.order() == order_G:
                    is_cyclic = True
                    break
            if not is_cyclic:
                return False
                
            # Check maximality among cyclic subgroups
            for f in group_F.elements:
                C = PermutationGroup([f])
                # If G is a subgroup of C
                if all(gen in C for gen in group_G.generators):
                    if C.order() > order_G:
                        return False
            return True
            
        h1 = is_maximal_cyclic(F, A) and is_maximal_cyclic(F, B)
    except Exception:
        h1 = False

    # H_2: A is not equal to B
    try:
        def groups_equal(G1, G2):
            if G1.order() != G2.order():
                return False
            for g in G1.generators:
                if g not in G2:
                    return False
            return True
            
        h2 = not groups_equal(A, B)
    except Exception:
        h2 = False

    # ¬Q: The intersection of A and B is not the trivial subgroup
    try:
        count = 0
        for g in A.elements:
            if g in B:
                count += 1
                if count > 1:
                    break
        neg_q = count > 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are maximal cyclic subgroups of F",
    "H_2: A is not equal to B",
    "¬Q: The intersection of A and B is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2