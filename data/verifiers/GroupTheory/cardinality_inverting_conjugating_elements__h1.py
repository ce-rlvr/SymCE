import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_inv(element):
    try:
        return element**-1
    except Exception:
        pass
    try:
        return ~element
    except Exception:
        pass
    return element.inv()

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G_raw, x, C_G_given, S_given = witness
            given_sets = True
        elif len(witness) == 2:
            G_raw, x = witness
            given_sets = False
        else:
            return [False, False, False, False]
            
        G = list(G_raw)
    except Exception:
        return [False, False, False, False]

    # H1: x is an element of G
    try:
        h1 = x in G
    except Exception:
        h1 = False

    # H2: C_G(x) is the centralizer of x in G
    try:
        C_G_computed = []
        for g in G:
            if g * x == x * g:
                C_G_computed.append(g)
        if given_sets:
            h2 = len(C_G_given) == len(C_G_computed) and all(c in C_G_computed for c in C_G_given)
            C_G = C_G_given
        else:
            h2 = True
            C_G = C_G_computed
    except Exception:
        h2 = False
        C_G = []

    # H3: S = {g \in G | gxg^{-1} = x^{-1}}
    try:
        S_computed = []
        inv_x = get_inv(x)
        for g in G:
            inv_g = get_inv(g)
            if g * x * inv_g == inv_x:
                S_computed.append(g)
                
        if given_sets:
            h3 = len(S_given) == len(S_computed) and all(s in S_computed for s in S_given)
            S = S_given
        else:
            h3 = True
            S = S_computed
    except Exception:
        h3 = False
        S = []

    # neg_Q: The cardinality of S is NOT either 0 or |C_G(x)|
    try:
        neg_q = (len(S) != 0) and (len(S) != len(C_G))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "H_2: C_G(x) is the centralizer of x in G",
    "H_3: S = {g in G | gxg^{-1} = x^{-1}}",
    "¬Q: The cardinality of S is neither 0 nor |C_G(x)|"
]

N_HYP = 3
NEG_Q_INDEX = 3