import sympy
from sympy.combinatorics import PermutationGroup
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
    """
    Helper function to check if H is a normal subgroup of G.
    For finite groups, it is sufficient to check that:
    1. All generators of H are in G.
    2. For every generator g of G and h of H, g * h * g^-1 is in H.
    """
    try:
        if not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
            return False
        
        # Check if H is a subgroup of G
        for gen in H.generators:
            if gen not in G:
                return False
                
        # Check normality
        for g in G.generators:
            g_inv = g**-1
            for h in H.generators:
                if (g * h * g_inv) not in H:
                    return False
                    
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness tuple (G_1, G_2, N_1, N_2), checks the remaining hypotheses
    and the negated conclusion.
    """
    try:
        G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G_1 and G_2 are groups
    try:
        h1 = isinstance(G1, PermutationGroup) and isinstance(G2, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N_1 is a normal subgroup of G_1
    try:
        h2 = is_normal_subgroup(N1, G1)
    except Exception:
        h2 = False
        
    # ¬Q: N_1 x N_2 is not a normal subgroup of G_1 x G_2, or the quotient is not isomorphic.
    # Mathematically, if N_1 is a normal subgroup of G_1, the conclusion holds 
    # if and only if N_2 is a normal subgroup of G_2.
    # Therefore, the conclusion fails iff N_2 is NOT a normal subgroup of G_2.
    try:
        neg_q = not is_normal_subgroup(N2, G2)
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G_1 and G_2 are groups",
    "H_2: N_1 is a normal subgroup of G_1",
    "¬Q: N_1 x N_2 is not a normal subgroup of G_1 x G_2, or the quotient is not isomorphic to (G_1/N_1) x (G_2/N_2)"
]

N_HYP = 2
NEG_Q_INDEX = 2