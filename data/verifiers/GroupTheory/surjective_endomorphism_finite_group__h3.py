import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        G, phi = witness
    except Exception:
        return [False, False, False]
    
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    # H2: phi is an endomorphism of G
    try:
        elements_list = list(G.elements)
        elements_set = set(elements_list)
        
        if callable(phi):
            phi_map = {g: phi(g) for g in elements_list}
        elif isinstance(phi, dict):
            phi_map = phi
        elif isinstance(phi, (list, tuple, set)):
            phi_map = dict(phi)
        else:
            phi_map = None
            
        h2 = False
        if phi_map is not None:
            h2 = True
            for g in elements_list:
                if g not in phi_map or phi_map[g] not in elements_set:
                    h2 = False
                    break
            if h2:
                for x in elements_list:
                    for y in elements_list:
                        if phi_map[x * y] != phi_map[x] * phi_map[y]:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False
        
    # neg_Q: phi is not an automorphism of G
    try:
        elements_list = list(G.elements)
        elements_set = set(elements_list)
        
        if callable(phi):
            phi_map_q = {g: phi(g) for g in elements_list}
        elif isinstance(phi, dict):
            phi_map_q = phi
        elif isinstance(phi, (list, tuple, set)):
            phi_map_q = dict(phi)
        else:
            phi_map_q = None
            
        if phi_map_q is None:
            neg_q = True
        else:
            is_endo = True
            for g in elements_list:
                if g not in phi_map_q or phi_map_q[g] not in elements_set:
                    is_endo = False
                    break
            if is_endo:
                for x in elements_list:
                    for y in elements_list:
                        if phi_map_q[x * y] != phi_map_q[x] * phi_map_q[y]:
                            is_endo = False
                            break
                    if not is_endo:
                        break
                        
            if not is_endo:
                neg_q = True
            else:
                image = set(phi_map_q[g] for g in elements_list)
                neg_q = len(image) < len(elements_list)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: \phi is an endomorphism of G",
    "¬Q: \phi is not an automorphism of G"
]

N_HYP = 2
NEG_Q_INDEX = 2