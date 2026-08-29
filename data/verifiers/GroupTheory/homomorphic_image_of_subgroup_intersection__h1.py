import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "H_2: A and B are subgroups of G",
    "¬Q: phi(A ∩ B) is not a subset of phi(A) ∩ phi(B)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Extract witness components
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            phi = witness['phi']
            A = witness['A']
            B = witness['B']
        elif isinstance(witness, tuple) and len(witness) == 5:
            G, H, phi, A, B = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: phi is a group homomorphism from G to H
    try:
        h1_ok = True
        if hasattr(G, 'elements'):
            G_elems = list(G.elements)
        else:
            G_elems = list(G)
            
        if hasattr(H, 'elements'):
            H_elems = list(H.elements)
        else:
            H_elems = list(H)
        
        if callable(phi):
            phi_func = phi
        else:
            phi_func = lambda x: phi[x]
            
        for g in G_elems:
            if phi_func(g) not in H_elems:
                h1_ok = False
                break
                
        if h1_ok:
            for x in G_elems:
                for y in G_elems:
                    if phi_func(x * y) != phi_func(x) * phi_func(y):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H_2: A and B are subgroups of G
    try:
        if hasattr(A, 'elements'):
            A_elems = set(A.elements)
        else:
            A_elems = set(A)
            
        if hasattr(B, 'elements'):
            B_elems = set(B.elements)
        else:
            B_elems = set(B)
            
        if hasattr(G, 'elements'):
            G_elems_set = set(G.elements)
        else:
            G_elems_set = set(G)
        
        h2_ok = A_elems.issubset(G_elems_set) and B_elems.issubset(G_elems_set)
        
        if h2_ok:
            if not A_elems:
                h2_ok = False
            else:
                for x in A_elems:
                    if x**-1 not in A_elems:
                        h2_ok = False
                        break
                    for y in A_elems:
                        if x * y not in A_elems:
                            h2_ok = False
                            break
                    if not h2_ok:
                        break
                        
        if h2_ok:
            if not B_elems:
                h2_ok = False
            else:
                for x in B_elems:
                    if x**-1 not in B_elems:
                        h2_ok = False
                        break
                    for y in B_elems:
                        if x * y not in B_elems:
                            h2_ok = False
                            break
                    if not h2_ok:
                        break
    except Exception:
        h2_ok = False

    # ¬Q: phi(A ∩ B) is not a subset of phi(A) ∩ phi(B)
    try:
        if hasattr(A, 'elements'):
            A_elems = set(A.elements)
        else:
            A_elems = set(A)
            
        if hasattr(B, 'elements'):
            B_elems = set(B.elements)
        else:
            B_elems = set(B)
            
        A_cap_B = A_elems.intersection(B_elems)
        
        if callable(phi):
            phi_func = phi
        else:
            phi_func = lambda x: phi[x]
            
        phi_A = set(phi_func(x) for x in A_elems)
        phi_B = set(phi_func(x) for x in B_elems)
        phi_A_cap_B = set(phi_func(x) for x in A_cap_B)
        
        phi_A_cap_phi_B = phi_A.intersection(phi_B)
        
        neg_q_ok = not phi_A_cap_B.issubset(phi_A_cap_phi_B)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]