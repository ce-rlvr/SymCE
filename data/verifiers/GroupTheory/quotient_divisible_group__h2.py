import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is an abelian group
    try:
        h1 = bool(G.is_abelian)
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h2 = bool(H.is_subgroup(G))
        elif hasattr(G, 'has_subgroup'):
            h2 = bool(G.has_subgroup(H))
        else:
            h2 = all(g in G for g in H.generators)
    except Exception:
        h2 = False
        
    # ¬Q: G/H is not a divisible abelian group
    try:
        if hasattr(G, 'is_divisible_quotient'):
            is_divisible = bool(G.is_divisible_quotient(H))
            neg_q = not is_divisible
        else:
            # A group G/H is divisible if for all x in G, and all n in 1..|G|, 
            # there exists y in G such that y^n * x^-1 in H.
            elements = list(G.elements)
            order_G = len(elements)
            
            is_divisible = True
            for n in range(1, order_G + 1):
                for x in elements:
                    x_inv = ~x
                    found = False
                    for y in elements:
                        if (y**n * x_inv) in H:
                            found = True
                            break
                    if not found:
                        is_divisible = False
                        break
                if not is_divisible:
                    break
                    
            neg_q = not is_divisible
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: H is a subgroup of G",
    "¬Q: G/H is not a divisible abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2