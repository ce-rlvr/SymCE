import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def is_dihedral(G):
    try:
        if not hasattr(G, 'order') or not hasattr(G, 'elements'):
            return False
        order = G.order()
        if order % 2 != 0:
            return False
        n = order // 2
        if n < 1:
            return False
        
        for r in G.elements:
            if r.order() == n:
                for s in G.elements:
                    if s.order() == 2:
                        if s * r * s == r**-1:
                            if PermutationGroup(r, s).order() == order:
                                return True
        return False
    except Exception:
        return False

def is_valid_R(G, R):
    try:
        if not isinstance(R, (set, list, tuple)):
            return False
        R_set = set(R)
        n = G.order() // 2
        
        for r in G.elements:
            if r.order() == n:
                C = set()
                curr = r
                for _ in range(n):
                    C.add(curr)
                    curr = curr * r
                expected_R = {g for g in G.elements if g.order() == 2 and g not in C}
                if R_set == expected_R:
                    return True
        return False
    except Exception:
        return False

def neg_Q_check(G, R):
    try:
        R_set = set(R)
        classes = []
        for g in R_set:
            found = False
            for cls in classes:
                if g in cls:
                    found = True
                    break
            if not found:
                new_class = set()
                for x in G.elements:
                    new_class.add(x * g * x**-1)
                classes.append(new_class)
        
        union_classes = set()
        for cls in classes:
            union_classes.update(cls)
        
        if union_classes != R_set:
            return True
        
        return len(classes) != 2
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        G, R = witness
    except Exception:
        return [False, False, False]
    
    h1 = is_dihedral(G)
    h2 = is_valid_R(G, R)
    neg_q = neg_Q_check(G, R)
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is the dihedral group of order 2n",
    "H_2: R is the set of all reflections (elements of order 2 that are not rotations) in G",
    "¬Q: R is not the disjoint union of exactly two conjugacy classes in G"
]

N_HYP = 2
NEG_Q_INDEX = 2