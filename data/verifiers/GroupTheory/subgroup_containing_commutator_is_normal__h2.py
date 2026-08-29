import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The commutator subgroup G' is contained in H",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G, H = witness
        if not hasattr(H, 'elements'):
            H = list(H)
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: The commutator subgroup G' is contained in H
    try:
        if hasattr(H, 'elements'):
            H_set = set(H.elements)
        else:
            H_set = set(H)
        G_prime = G.derived_subgroup()
        h2 = set(G_prime.elements).issubset(H_set)
    except Exception:
        h2 = False
        
    # ¬Q: H is not a normal subgroup of G
    try:
        if not isinstance(G, PermutationGroup):
            neg_q = True
        else:
            if hasattr(H, 'elements'):
                H_set = set(H.elements)
            else:
                H_set = set(H)
                
            G_elements = set(G.elements)
            
            is_subgroup = True
            if not H_set.issubset(G_elements):
                is_subgroup = False
            elif not H_set:
                is_subgroup = False
            else:
                for a in H_set:
                    for b in H_set:
                        if a * (~b) not in H_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                        
            is_normal = True
            if is_subgroup:
                for h in H_set:
                    for g in G_elements:
                        if g * h * (~g) not in H_set:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                        
            neg_q = not (is_subgroup and is_normal)
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]