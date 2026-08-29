import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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
        return [False, False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and all(g in G for g in H.generators)
    except Exception:
        h2 = False

    # H_3: The index of H in G is exactly 2
    try:
        h3 = (G.order() == 2 * H.order())
    except Exception:
        h3 = False

    # H_4: C is a conjugacy class of G
    try:
        C_set = set(C)
        if not C_set:
            h4 = False
        elif not all(isinstance(c, Permutation) and c in G for c in C_set):
            h4 = False
        else:
            c = next(iter(C_set))
            G_elements = list(G.generate())
            G_class = set(g * c * (~g) for g in G_elements)
            h4 = (C_set == G_class)
    except Exception:
        h4 = False

    # neg_Q: C is neither a single conjugacy class in H nor the disjoint union of exactly two conjugacy classes of H of equal size
    try:
        C_set = set(C)
        if not all(isinstance(c, Permutation) and c in H for c in C_set):
            q = False
        else:
            classes = []
            unseen = set(C_set)
            H_elements = list(H.generate())
            while unseen:
                c = unseen.pop()
                h_class = set(h * c * (~h) for h in H_elements)
                classes.append(h_class)
                unseen -= h_class
            
            if len(classes) == 1:
                q = True
            elif len(classes) == 2 and len(classes[0]) == len(classes[1]):
                q = True
            else:
                q = False
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: The index of H in G is exactly 2",
    "H_4: C is a conjugacy class of G",
    "not Q: C is neither a single conjugacy class in H nor the disjoint union of exactly two conjugacy classes of H of equal size"
]

N_HYP = 4
NEG_Q_INDEX = 4