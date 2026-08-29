import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def check_is_subgroup(sub, supergroup):
    try:
        if hasattr(sub, 'is_subgroup'):
            return sub.is_subgroup(supergroup)
    except Exception:
        pass
    try:
        try:
            elems = list(sub.generate())
        except Exception:
            elems = list(sub.elements)
        for h in elems:
            if not supergroup.contains(h):
                return False
        return True
    except Exception:
        return False

def check_is_normal(sub, supergroup):
    try:
        if hasattr(sub, 'is_normal'):
            return sub.is_normal(supergroup)
    except Exception:
        pass
    try:
        try:
            elems_sub = list(sub.generate())
        except Exception:
            elems_sub = list(sub.elements)
        try:
            elems_sup = list(supergroup.generate())
        except Exception:
            elems_sup = list(supergroup.elements)
        for g in elems_sup:
            for h in elems_sub:
                if not sub.contains(g * h * ~g):
                    return False
        return True
    except Exception:
        return False

def check_is_solvable(group):
    try:
        if hasattr(group, 'is_solvable'):
            val = group.is_solvable
            if callable(val):
                return val()
            return val
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: Let H and K be normal subgroups of G
    try:
        h1 = (check_is_subgroup(H, G) and check_is_subgroup(K, G) and 
              check_is_normal(H, G) and check_is_normal(K, G))
    except Exception:
        h1 = False

    # H_2: Assume H is a solvable group
    try:
        h2 = check_is_solvable(H)
    except Exception:
        h2 = False

    # H_3: Assume K is a solvable group
    try:
        h3 = check_is_solvable(K)
    except Exception:
        h3 = False

    # neg_Q: The product HK is not a normal solvable subgroup of G
    try:
        try:
            elements_H = list(H.generate())
        except Exception:
            elements_H = list(H.elements)
            
        try:
            elements_K = list(K.generate())
        except Exception:
            elements_K = list(K.elements)
            
        HK_set = set()
        for h in elements_H:
            for k in elements_K:
                HK_set.add(h * k)
        
        HK_group = PermutationGroup(list(HK_set))
        is_HK_subgroup = (HK_group.order() == len(HK_set))
        
        if not is_HK_subgroup:
            neg_q = True
        else:
            is_normal = check_is_normal(HK_group, G)
            is_solvable = check_is_solvable(HK_group)
            neg_q = not (is_normal and is_solvable)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H and K are normal subgroups of G",
    "H_2: H is a solvable group",
    "H_3: K is a solvable group",
    "¬Q: The product HK is not a normal solvable subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3