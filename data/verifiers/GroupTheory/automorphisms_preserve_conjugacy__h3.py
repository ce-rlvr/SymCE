import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, x, y, phi = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: x and y are elements of G
    try:
        h2 = x in G and y in G
    except Exception:
        h2 = False

    # H3: phi is an automorphism of G
    try:
        if isinstance(phi, dict):
            phi_func = lambda g: phi[g]
        else:
            phi_func = phi
            
        elements = list(G.elements)
        
        mapped_elements = []
        is_bijection = True
        for g in elements:
            mg = phi_func(g)
            if mg not in G:
                is_bijection = False
                break
            mapped_elements.append(mg)
            
        if is_bijection:
            is_bijection = len(set(mapped_elements)) == len(elements)
            
        if is_bijection:
            is_homo = True
            for a in elements:
                for b in elements:
                    if phi_func(a * b) != phi_func(a) * phi_func(b):
                        is_homo = False
                        break
                if not is_homo:
                    break
            h3 = is_homo
        else:
            h3 = False
    except Exception:
        h3 = False

    # Negated Conclusion: phi(y) and phi(x) are not conjugate in G
    try:
        if isinstance(phi, dict):
            phi_func = lambda g: phi[g]
        else:
            phi_func = phi
            
        phi_x = phi_func(x)
        phi_y = phi_func(y)
        
        elements = list(G.elements)
        are_conjugate = False
        for h in elements:
            if phi_y == h * phi_x * ~h:
                are_conjugate = True
                break
        neg_q = not are_conjugate
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are elements of G",
    "H_3: phi is an automorphism of G",
    "¬Q: phi(x) and phi(y) are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3