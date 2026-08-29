import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros
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

def apply_act(act, g, a):
    if callable(act):
        return act(g, a)
    elif isinstance(act, dict):
        return act[(g, a)]
    else:
        raise TypeError("act must be callable or dict")

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            X = witness['X']
            act = witness['act']
            x = witness['x']
            y = witness['y']
        else:
            G, X, act, x, y = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
    except Exception:
        elements = []

    try:
        h1 = False
        if hasattr(G, 'is_group') and G.is_group:
            h1 = True
        elif type(G).__name__ == 'PermutationGroup':
            h1 = True
        elif elements:
            h1 = True
    except Exception:
        h1 = False

    try:
        X_list = list(X)
        h2 = True
        if not X_list:
            h2 = False
        else:
            for a in X_list:
                for b in X_list:
                    if not any(apply_act(act, g, a) == b for g in elements):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    try:
        X_list = list(X)
        h3 = x in X_list
    except Exception:
        h3 = False

    try:
        X_list = list(X)
        h4 = y in X_list
    except Exception:
        h4 = False

    try:
        stab_x = []
        for g in elements:
            if apply_act(act, g, x) == x:
                if g not in stab_x:
                    stab_x.append(g)
                
        stab_y = []
        for g in elements:
            if apply_act(act, g, y) == y:
                if g not in stab_y:
                    stab_y.append(g)
                
        q = False
        for g in elements:
            try:
                g_inv = g**-1
            except Exception:
                g_inv = ~g
                
            conj = []
            for h in stab_x:
                c = g * h * g_inv
                if c not in conj:
                    conj.append(c)
            
            if len(conj) == len(stab_y) and all(c in stab_y for c in conj):
                q = True
                break
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts transitively on X",
    "H_3: x is an element of X",
    "H_4: y is an element of X",
    "¬Q: There is no element g in G such that Stab_G(y) = g * Stab_G(x) * g^{-1}"
]

N_HYP = 4
NEG_Q_INDEX = 4