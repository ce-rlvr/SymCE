import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.permutations import Permutation
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

def get_elements(obj):
    if hasattr(obj, 'elements'):
        return set(obj.elements)
    elif hasattr(obj, 'generate') and callable(obj.generate):
        return set(obj.generate())
    else:
        try:
            return set(obj)
        except Exception:
            return set()

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False
        
    try:
        elems_G = get_elements(G)
        elems_K = get_elements(K)
        h3 = len(elems_G) > 0 and len(elems_K) > 0 and isinstance(K, PermutationGroup) and K.is_subgroup(G)
    except Exception:
        h3 = False
        
    try:
        elems_G = get_elements(G)
        elems_H = get_elements(H)
        elems_K = get_elements(K)
        intersection = elems_H.intersection(elems_K)
        
        if len(intersection) == 0:
            Q = False
        else:
            Q = len(elems_H) * len(elems_K) <= len(elems_G) * len(intersection)
            
        neg_q = not Q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: The index of K in G is finite",
    "not Q: The index of H intersect K in H is not finite or not less than or equal to the index of K in G"
]

N_HYP = 3
NEG_Q_INDEX = 3