import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, x = witness
    except Exception:
        return [False, False, False]
        
    # H1: The order of G is an odd integer
    try:
        if hasattr(G, 'order'):
            order_attr = getattr(G, 'order')
            if callable(order_attr):
                order = order_attr()
            else:
                order = order_attr
        elif hasattr(G, 'elements'):
            order = len(list(G.elements))
        else:
            order = len(list(G))
        h1 = (int(order) % 2 == 1)
    except Exception:
        h1 = False
        
    # H2: x is an element of G such that x is not the identity element
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        if hasattr(G, 'identity'):
            identity = G.identity
        else:
            identity = elements[0]**0
            
        h2 = (x in elements) and (x != identity)
    except Exception:
        h2 = False
        
    # neg_Q: x is conjugate to x^-1 in G
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        x_inv = x**-1
        neg_q = False
        for g in elements:
            try:
                g_inv = g**-1
                if g * x * g_inv == x_inv or g_inv * x * g == x_inv:
                    neg_q = True
                    break
            except Exception:
                pass
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is an odd integer",
    "H_2: x is an element of G such that x is not the identity element",
    "¬Q: x is conjugate to x^(-1) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2