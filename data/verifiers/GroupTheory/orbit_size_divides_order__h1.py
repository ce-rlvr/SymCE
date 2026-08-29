import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        G, X, action, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: X is a set
    try:
        h1 = isinstance(X, (set, list, tuple))
    except Exception:
        h1 = False
        
    try:
        G_list = list(G)
        X_list = list(X)
    except Exception:
        return [h1, False, False, False]
        
    # H2: G acts on X
    try:
        h2 = True
        for g in G_list:
            for y in X_list:
                try:
                    res = action(g, y)
                except TypeError:
                    res = action[(g, y)]
                if res not in X_list:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False
        
    # H3: x is an element of X
    try:
        h3 = x in X_list
    except Exception:
        h3 = False
        
    # neg_Q: |Orb_G(x)| does not divide |G|
    try:
        orbit = []
        for g in G_list:
            try:
                res = action(g, x)
            except TypeError:
                res = action[(g, x)]
            if res not in orbit:
                orbit.append(res)
        orbit_size = len(orbit)
        g_size = len(G_list)
        
        if orbit_size == 0:
            neg_q = False
        else:
            neg_q = (g_size % orbit_size != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "H_3: x is an element of X",
    "¬Q: The cardinality of the orbit of x does not divide the order of G"
]

N_HYP = 3
NEG_Q_INDEX = 3