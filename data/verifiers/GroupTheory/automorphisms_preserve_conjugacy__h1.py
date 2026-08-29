import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard algebra objects
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

def in_G(G, a):
    if hasattr(G, 'contains'):
        try:
            if G.contains(a): return True
        except Exception:
            pass
    if hasattr(G, 'elements'):
        try:
            if a in G.elements: return True
        except Exception:
            pass
    try:
        if a in G: return True
    except Exception:
        pass
    return False

def apply_phi(phi, a):
    if isinstance(phi, dict):
        return phi[a]
    return phi(a)

def conditions(witness) -> list[bool]:
    try:
        G, x, y, g, phi = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: x and y are elements of G
    try:
        h1 = in_G(G, x) and in_G(G, y)
    except Exception:
        h1 = False
        
    # H_2: There exists an element g in G such that y = gxg^{-1}
    try:
        h2 = in_G(G, g) and (y == g * x * g**-1)
    except Exception:
        h2 = False
        
    # H_3: phi is an automorphism of G
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        mapped_elements = []
        for a in elements:
            ma = apply_phi(phi, a)
            if not in_G(G, ma):
                raise ValueError
            mapped_elements.append(ma)
            
        # Check bijection
        try:
            is_bijection = len(mapped_elements) == len(elements) and len(set(mapped_elements)) == len(elements)
        except TypeError:
            unique = []
            for m in mapped_elements:
                if m not in unique:
                    unique.append(m)
            is_bijection = len(mapped_elements) == len(elements) and len(unique) == len(elements)
            
        # Check homomorphism (preserves binary operation)
        is_homo = True
        for a in elements:
            for b in elements:
                ma = apply_phi(phi, a)
                mb = apply_phi(phi, b)
                mab = apply_phi(phi, a * b)
                if mab != ma * mb:
                    is_homo = False
                    break
            if not is_homo:
                break
                
        h3 = is_bijection and is_homo
    except Exception:
        h3 = False
        
    # ¬Q: phi(y) != phi(g) * phi(x) * phi(g)^{-1}
    try:
        py = apply_phi(phi, y)
        pg = apply_phi(phi, g)
        px = apply_phi(phi, x)
        neg_q = (py != pg * px * pg**-1)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "H_2: There exists an element g in G such that y = gxg^{-1}",
    "H_3: phi is an automorphism of G",
    "¬Q: phi(y) != phi(g) * phi(x) * phi(g)^{-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3