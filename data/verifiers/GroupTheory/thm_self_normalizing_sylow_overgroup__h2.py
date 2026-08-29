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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G such that N_G(P) is a subgroup of H",
    "¬Q: The normalizer N_G(H) is not equal to H"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) == 3:
            G, H, P = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group (and P is a valid subgroup of G)
    try:
        if not hasattr(G, 'elements'):
            h1 = False
        else:
            if hasattr(P, 'is_subgroup'):
                h1 = bool(P.is_subgroup(G))
            else:
                g_elements = set(G.elements)
                h1 = all(p in g_elements for p in P.elements)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G such that N_G(P) is a subgroup of H
    try:
        if not h1:
            h2 = False
        else:
            if hasattr(H, 'is_subgroup'):
                is_sub = H.is_subgroup(G)
            else:
                g_elements = set(G.elements)
                is_sub = all(h in g_elements for h in H.elements)
            
            if not is_sub:
                h2 = False
            else:
                h_elements = set(H.elements)
                p_elements = set(P.elements)
                p_gens = P.generators
                
                n_g_p_in_h = True
                for g in G.elements:
                    normalizes = True
                    try:
                        g_inv = ~g
                    except Exception:
                        g_inv = g**-1
                        
                    for p in p_gens:
                        if (g * p * g_inv) not in p_elements:
                            normalizes = False
                            break
                            
                    if normalizes:
                        if g not in h_elements:
                            n_g_p_in_h = False
                            break
                h2 = bool(n_g_p_in_h)
    except Exception:
        h2 = False

    # neg_Q: N_G(H) != H
    try:
        if not h1:
            neg_q = False
        else:
            h_elements = set(H.elements)
            h_gens = H.generators
            
            n_g_h_equals_h = True
            for g in G.elements:
                normalizes = True
                try:
                    g_inv = ~g
                except Exception:
                    g_inv = g**-1
                    
                for h in h_gens:
                    if (g * h * g_inv) not in h_elements:
                        normalizes = False
                        break
                        
                if normalizes:
                    if g not in h_elements:
                        n_g_h_equals_h = False
                        break
            neg_q = not n_g_h_equals_h
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]