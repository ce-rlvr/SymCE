import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    try:
        G, x = witness
    except Exception:
        return [False, False]
        
    # H_1: G is a finite group
    try:
        if not hasattr(G, 'elements'):
            h1 = False
        else:
            order = G.order() if callable(G.order) else G.order
            h1 = bool(order > 0 and order != sympy.oo)
    except Exception:
        h1 = False
        
    # ¬Q: The size of the conjugacy class of x is NOT equal to the index of C_G(x) in G
    try:
        # Determine if x is a subset/subgroup or a single element/tuple
        if hasattr(x, 'elements'):
            x_elements = set(x.elements)
            is_subset = True
        elif isinstance(x, (set, frozenset)):
            x_elements = set(x)
            is_subset = True
        elif isinstance(x, (list, tuple)):
            x_elements = tuple(x)
            is_subset = False
        else:
            x_elements = x
            is_subset = False
            
        orbit = set()
        C_G_x = set()
        
        order = G.order() if callable(G.order) else G.order
        
        for g in list(G.elements):
            g_inv = g**-1
            
            # Compute conjugate of x by g
            if is_subset:
                conj = frozenset(g * e * g_inv for e in x_elements)
            elif isinstance(x_elements, tuple):
                conj = tuple(g * e * g_inv for e in x_elements)
            else:
                conj = g * x_elements * g_inv
            orbit.add(conj)
            
            # Check if g is in the centralizer C_G(x)
            if is_subset:
                # Centralizer of a subset: commutes with every element
                if all(g * e == e * g for e in x_elements):
                    C_G_x.add(g)
            elif isinstance(x_elements, tuple):
                if all(g * e == e * g for e in x_elements):
                    C_G_x.add(g)
            else:
                if g * x_elements == x_elements * g:
                    C_G_x.add(g)
                    
        size_conjugacy_class = len(orbit)
        
        # The conclusion is: size_conjugacy_class == order / len(C_G_x)
        # We check if this FAILS (i.e., size_conjugacy_class * len(C_G_x) != order)
        neg_q = (size_conjugacy_class * len(C_G_x) != order)
    except Exception:
        neg_q = False
        
    return [h1, bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The size of the conjugacy class of x is not equal to the index of C_G(x) in G"
]

N_HYP = 1
NEG_Q_INDEX = 1