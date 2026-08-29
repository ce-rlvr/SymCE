import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "H_2: A is a subgroup of G",
    "H_3: B is a subgroup of G",
    "¬Q: phi(AB) != phi(A)phi(B)"
]

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            phi = witness['phi']
            A = witness['A']
            B = witness['B']
        else:
            G, H, phi, A, B = witness
    except Exception:
        return [False, False, False, False]

    def get_elements(obj):
        if hasattr(obj, 'generate'):
            return set(obj.generate())
        elif hasattr(obj, 'elements'):
            return set(obj.elements)
        else:
            return set(obj)

    try:
        G_elements = get_elements(G)
        H_elements = get_elements(H)
        
        h1 = True
        if isinstance(phi, dict):
            phi_func = lambda x: phi[x]
        else:
            phi_func = phi
            
        for g in G_elements:
            if phi_func(g) not in H_elements:
                h1 = False
                break
                
        if h1:
            for g1 in G_elements:
                for g2 in G_elements:
                    if phi_func(g1 * g2) != phi_func(g1) * phi_func(g2):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    try:
        A_set = get_elements(A)
        h2 = True
        if not A_set.issubset(G_elements):
            h2 = False
        elif not A_set:
            h2 = False
        else:
            for a1 in A_set:
                if a1**-1 not in A_set:
                    h2 = False
                    break
                for a2 in A_set:
                    if a1 * a2 not in A_set:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    try:
        B_set = get_elements(B)
        h3 = True
        if not B_set.issubset(G_elements):
            h3 = False
        elif not B_set:
            h3 = False
        else:
            for b1 in B_set:
                if b1**-1 not in B_set:
                    h3 = False
                    break
                for b2 in B_set:
                    if b1 * b2 not in B_set:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    try:
        AB = set(a * b for a in A_set for b in B_set)
        phi_AB = set(phi_func(x) for x in AB)
        
        phi_A = set(phi_func(a) for a in A_set)
        phi_B = set(phi_func(b) for b in B_set)
        phi_A_phi_B = set(x * y for x in phi_A for y in phi_B)
        
        neg_q = (phi_AB != phi_A_phi_B)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]