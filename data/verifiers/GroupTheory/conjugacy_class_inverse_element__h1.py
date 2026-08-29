import sympy
from sympy.combinatorics import Permutation
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def elements_of(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return list(G)

def is_eq_sets(A, B):
    list_A = list(A)
    list_B = list(B)
    for a in list_A:
        if a not in list_B:
            return False
    for b in list_B:
        if b not in list_A:
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        G, x, C = witness
    except Exception:
        return [False, False, False]
    
    # H_1: x is an element of G
    try:
        if hasattr(G, 'contains'):
            h1 = bool(G.contains(x))
        else:
            h1 = bool(x in G)
    except Exception:
        h1 = False

    # H_2: C is the conjugacy class of x in G
    try:
        G_elements = elements_of(G)
        conj_x = []
        for g in G_elements:
            try:
                try:
                    inv_g = g**-1
                except Exception:
                    inv_g = g.inv()
                elem = g * x * inv_g
                if elem not in conj_x:
                    conj_x.append(elem)
            except Exception:
                pass
        h2 = is_eq_sets(C, conj_x)
    except Exception:
        h2 = False

    # ¬Q: The set of inverses C^{-1} is not exactly the conjugacy class of the inverse element x^{-1} in G.
    try:
        G_elements = elements_of(G)
        try:
            x_inv = x**-1
        except Exception:
            x_inv = x.inv()
            
        C_inv = []
        for c in C:
            try:
                inv_c = c**-1
            except Exception:
                inv_c = c.inv()
            if inv_c not in C_inv:
                C_inv.append(inv_c)
                
        conj_x_inv = []
        for g in G_elements:
            try:
                try:
                    inv_g = g**-1
                except Exception:
                    inv_g = g.inv()
                elem = g * x_inv * inv_g
                if elem not in conj_x_inv:
                    conj_x_inv.append(elem)
            except Exception:
                pass
            
        neg_q = not is_eq_sets(C_inv, conj_x_inv)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "H_2: C is the conjugacy class of x in G",
    "¬Q: The set of inverses C^{-1} is not exactly the conjugacy class of x^{-1} in G"
]

N_HYP = 2
NEG_Q_INDEX = 2