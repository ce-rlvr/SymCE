import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        G, H, C = witness
    except Exception:
        return [False] * 5

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: H is a subgroup of G
    try:
        h2_ok = isinstance(H, PermutationGroup) and all(g in G for g in H.generators)
    except Exception:
        h2_ok = False

    # H_3: The index of H in G is exactly 2
    try:
        h3_ok = G.order() == 2 * H.order()
    except Exception:
        h3_ok = False

    # H_4: C is a subset of H
    try:
        C_set = set(C)
        h4_ok = all(c in H for c in C_set)
    except Exception:
        h4_ok = False

    # ¬Q: C is neither a single conjugacy class in H, nor the disjoint union of exactly two conjugacy classes of H of equal size
    try:
        C_set = set(C)
        H_elements = list(H.generate())
        is_conclusion_true = False
        
        if C_set:
            classes = []
            unseen = set(C_set)
            is_union = True
            
            while unseen:
                x = unseen.pop()
                # Compute the conjugacy class of x in H
                c_class = set(h * x * ~h for h in H_elements)
                
                if not c_class.issubset(C_set):
                    is_union = False
                    break
                    
                classes.append(c_class)
                unseen -= c_class
                
            if is_union:
                if len(classes) == 1:
                    is_conclusion_true = True
                elif len(classes) == 2 and len(classes[0]) == len(classes[1]):
                    is_conclusion_true = True
                    
        neg_q_ok = not is_conclusion_true
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: The index of H in G is exactly 2",
    "H_4: C is a subset of H",
    "¬Q: C is neither a single conjugacy class in H, nor the disjoint union of exactly two conjugacy classes of H of equal size"
]

N_HYP = 4
NEG_Q_INDEX = 4