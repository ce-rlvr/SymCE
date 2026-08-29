import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def is_subgroup(sub, G):
    if not isinstance(sub, PermutationGroup):
        return False
    for g in sub.generators:
        if g not in G:
            return False
    return True

def is_normal(G, sub):
    if not is_subgroup(sub, G):
        return False
    for g in G.generators:
        for h in sub.generators:
            conj = g * h * (~g)
            if conj not in sub:
                return False
    return True

def is_quotient_solvable(G, K):
    curr = G
    while True:
        if all(g in K for g in curr.generators):
            return True
        nxt = curr.derived_subgroup()
        if curr.order() == nxt.order():
            return False
        curr = nxt

def is_quotient_intersection_solvable(G, H, K):
    curr = G
    while True:
        if all((g in H and g in K) for g in curr.generators):
            return True
        nxt = curr.derived_subgroup()
        if curr.order() == nxt.order():
            return False
        curr = nxt

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H and K are normal subgroups of G
    try:
        h2 = is_normal(G, H) and is_normal(G, K)
    except Exception:
        h2 = False
        
    # H_3: The quotient group G/K is solvable
    try:
        h3 = is_quotient_solvable(G, K)
    except Exception:
        h3 = False
        
    # ¬Q: The quotient group G/(H \cap K) is not solvable
    try:
        neg_q = not is_quotient_intersection_solvable(G, H, K)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H and K are normal subgroups of G",
    "H_3: The quotient group G/K is solvable",
    "¬Q: The quotient group G/(H \\cap K) is not solvable"
]

N_HYP = 3
NEG_Q_INDEX = 3