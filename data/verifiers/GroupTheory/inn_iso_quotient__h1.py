import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: Inn(G) is the inner automorphism group of G",
    "¬Q: Inn(G) is not isomorphic to the quotient group G/Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, Z, Inn = witness
            
            # Check H1: Z(G) is the center of G
            try:
                H1 = (Z == G.center())
            except Exception:
                H1 = False
                
            # Check H2: Inn(G) is the inner automorphism group of G
            try:
                if isinstance(G, PermutationGroup):
                    elements = list(G.elements)
                    gens = []
                    for g in G.generators:
                        p = Permutation([elements.index(g * x * ~g) for x in elements])
                        gens.append(p)
                    if not gens:
                        gens = [Permutation(len(elements) - 1 if elements else 0)]
                    expected_Inn = PermutationGroup(gens)
                    try:
                        H2 = bool(Inn.is_isomorphic(expected_Inn))
                    except Exception:
                        H2 = (Inn == expected_Inn)
                else:
                    H2 = (Inn == G.inner_automorphisms())
            except Exception:
                H2 = False
                
            # Check ¬Q: Inn(G) is NOT isomorphic to G/Z(G)
            try:
                if isinstance(G, PermutationGroup):
                    Q_grp = G.quotient_group(Z)
                elif hasattr(G, 'quotient_group'):
                    Q_grp = G.quotient_group(Z)
                else:
                    Q_grp = G.quotient(Z)
                Q = bool(Inn.is_isomorphic(Q_grp))
                neg_Q = not Q
            except Exception:
                neg_Q = False
                
        else:
            G = witness
            
            # Check H1: Z(G) is the center of G
            try:
                Z = G.center()
                H1 = True
            except Exception:
                H1 = False
                
            # Check H2: Inn(G) is the inner automorphism group of G
            try:
                if isinstance(G, PermutationGroup):
                    elements = list(G.elements)
                    gens = []
                    for g in G.generators:
                        p = Permutation([elements.index(g * x * ~g) for x in elements])
                        gens.append(p)
                    if not gens:
                        gens = [Permutation(len(elements) - 1 if elements else 0)]
                    Inn = PermutationGroup(gens)
                    H2 = True
                else:
                    Inn = G.inner_automorphisms()
                    H2 = True
            except Exception:
                H2 = False
                
            # Check ¬Q: Inn(G) is NOT isomorphic to G/Z(G)
            try:
                if isinstance(G, PermutationGroup):
                    Q_grp = G.quotient_group(Z)
                elif hasattr(G, 'quotient_group'):
                    Q_grp = G.quotient_group(Z)
                else:
                    Q_grp = G.quotient(Z)
                Q = bool(Inn.is_isomorphic(Q_grp))
                neg_Q = not Q
            except Exception:
                neg_Q = False
                
    except Exception:
        pass
        
    return [H1, H2, neg_Q]