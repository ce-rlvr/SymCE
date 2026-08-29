import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
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
    "H_1: G is a group",
    "H_2: x and y are elements of G",
    "H_3: x^2 = e and y^2 = e",
    "¬Q: g is not conjugate to g^-1 in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, x, y = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
        elif hasattr(G, 'elements') and hasattr(G, 'identity'):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: x and y are elements of G
    try:
        if hasattr(G, '__contains__'):
            h2 = bool((x in G) and (y in G))
        else:
            elements = list(G.elements)
            h2 = bool((x in elements) and (y in elements))
    except Exception:
        h2 = False
        
    # H3: x^2 = e and y^2 = e
    try:
        e = G.identity
        h3 = bool((x**2 == e) and (y**2 == e))
    except Exception:
        h3 = False
        
    # ¬Q: g is not conjugate to g^-1 in G
    try:
        g = x * y
        try:
            g_inv = ~g
        except Exception:
            g_inv = g**-1
            
        is_conj = False
        for h in G.elements:
            try:
                h_inv = ~h
            except Exception:
                h_inv = h**-1
                
            # Check both left and right conjugation conventions to be absolutely safe
            if h_inv * g * h == g_inv or h * g * h_inv == g_inv:
                is_conj = True
                break
                
        neg_q = not is_conj
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]