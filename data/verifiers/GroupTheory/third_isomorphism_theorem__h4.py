import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_normal_subgroup(H, G):
    """Helper to check if H is a normal subgroup of G."""
    try:
        if not H.is_subgroup(G):
            return False
        # Check if g * h * g^-1 is in H for all generators g of G and h of H
        for g in G.generators:
            for h in H.generators:
                if (g * h * ~g) not in H:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, N, K = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = is_normal_subgroup(N, G)
    except Exception:
        h2 = False
        
    try:
        h3 = is_normal_subgroup(K, G)
    except Exception:
        h3 = False
        
    try:
        # The Third Isomorphism Theorem requires N to be a subgroup of K.
        # If N is not a subgroup of K, the quotient K/N is not well-defined as a standard group,
        # and the conclusion fails. For finite groups, (G/N)/(KN/N) is isomorphic to G/K 
        # if and only if N is a subgroup of K.
        neg_q = not N.is_subgroup(K)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: K is a normal subgroup of G",
    "¬Q: K/N is not a normal subgroup of G/N, or (G/N)/(K/N) is not isomorphic to G/K"
]

N_HYP = 3
NEG_Q_INDEX = 3