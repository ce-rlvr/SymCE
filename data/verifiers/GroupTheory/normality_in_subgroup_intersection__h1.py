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

def is_normal(N, G):
    """Check if N is a normal subgroup of G."""
    # Check if N is a subgroup of G
    if not all(g in G for g in N.generators):
        return False
    # Check conjugation for all generators
    for n in N.generators:
        for g in G.generators:
            try:
                g_inv = ~g
            except Exception:
                g_inv = g**-1
            if (g_inv * n * g) not in N:
                return False
            if (g * n * g_inv) not in N:
                return False
    return True

def intersect_groups(N, H):
    """Return the intersection of two permutation groups as a new group."""
    elements = [g for g in N.elements if g in H]
    return PermutationGroup(*elements)

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: N is a normal subgroup of G
    try:
        h1_ok = is_normal(N, G)
    except Exception:
        h1_ok = False
        
    # H_2: H is a subgroup of G
    try:
        h2_ok = all(g in G for g in H.generators)
    except Exception:
        h2_ok = False
        
    # neg_Q: The intersection N \cap H is NOT a normal subgroup of H
    try:
        N_cap_H = intersect_groups(N, H)
        neg_q_ok = not is_normal(N_cap_H, H)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "¬Q: The intersection N \\cap H is not a normal subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2