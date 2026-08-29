import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = getattr(G, 'is_group', False) or isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = H.is_subgroup(G)
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            elements = list(G.generate())
            conjugates = []
            normalizer_order = 0
            
            for g in elements:
                if not H.generators:
                    conj_H = H
                else:
                    conj_gens = [g * h * ~g for h in H.generators]
                    conj_H = PermutationGroup(conj_gens)
                
                if conj_H.is_subgroup(H) and H.is_subgroup(conj_H):
                    normalizer_order += 1
                    
                is_new = True
                for c in conjugates:
                    if conj_H.is_subgroup(c) and c.is_subgroup(conj_H):
                        is_new = False
                        break
                if is_new:
                    conjugates.append(conj_H)
            
            index = len(elements) // normalizer_order
            num_conjugates = len(conjugates)
            neg_q = (num_conjugates != index)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "¬Q: The number of distinct conjugate subgroups of H in G is not exactly the index of N_G(H) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2