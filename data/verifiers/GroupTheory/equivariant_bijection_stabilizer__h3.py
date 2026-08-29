import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        X = list(witness['X'])
        Y = list(witness['Y'])
        action_X = witness['action_X']
        action_Y = witness['action_Y']
        f = witness['f']
        x_elem = witness['x']
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on sets X and Y
    h1 = False
    try:
        if hasattr(G, 'elements') and hasattr(G, 'identity'):
            elements = list(G.elements)
            id_elem = G.identity
            
            h1_X_left = True
            h1_X_right = True
            for x in X:
                if action_X(id_elem, x) != x:
                    h1_X_left = False
                    h1_X_right = False
                for g in elements:
                    gx = action_X(g, x)
                    if gx not in X:
                        h1_X_left = False
                        h1_X_right = False
                    for h in elements:
                        if action_X(g, action_X(h, x)) != action_X(g * h, x):
                            h1_X_left = False
                        if action_X(h, action_X(g, x)) != action_X(g * h, x):
                            h1_X_right = False
            h1_X = h1_X_left or h1_X_right
            
            h1_Y_left = True
            h1_Y_right = True
            for y in Y:
                if action_Y(id_elem, y) != y:
                    h1_Y_left = False
                    h1_Y_right = False
                for g in elements:
                    gy = action_Y(g, y)
                    if gy not in Y:
                        h1_Y_left = False
                        h1_Y_right = False
                    for h in elements:
                        if action_Y(g, action_Y(h, y)) != action_Y(g * h, y):
                            h1_Y_left = False
                        if action_Y(h, action_Y(g, y)) != action_Y(g * h, y):
                            h1_Y_right = False
            h1_Y = h1_Y_left or h1_Y_right
            
            h1 = h1_X and h1_Y
    except Exception:
        h1 = False

    # H_2: f: X -> Y is a bijection
    h2 = False
    try:
        h2_valid = True
        for x in X:
            fx = f(x)
            if fx not in Y:
                h2_valid = False
                break
        
        if h2_valid:
            # Check injectivity
            for i in range(len(X)):
                for j in range(i + 1, len(X)):
                    if f(X[i]) == f(X[j]) and X[i] != X[j]:
                        h2_valid = False
                        break
            
            # Check surjectivity
            for y in Y:
                found = False
                for x in X:
                    if f(x) == y:
                        found = True
                        break
                if not found:
                    h2_valid = False
                    break
                    
        h2 = h2_valid
    except Exception:
        h2 = False

    # H_3: x is an element of X
    h3 = False
    try:
        if x_elem in X:
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: The stabilizer of x in G is NOT exactly equal to the stabilizer of f(x) in G
    neg_q = False
    try:
        elements = list(G.elements)
        stab_x = set()
        for g in elements:
            if action_X(g, x_elem) == x_elem:
                stab_x.add(g)
                
        fx = f(x_elem)
        stab_fx = set()
        for g in elements:
            if action_Y(g, fx) == fx:
                stab_fx.add(g)
                
        if stab_x != stab_fx:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on sets X and Y",
    "H_2: f: X -> Y is a bijection",
    "H_3: x is an element of X",
    "¬Q: The stabilizer of x in G is not exactly equal to the stabilizer of f(x) in G"
]

N_HYP = 3
NEG_Q_INDEX = 3