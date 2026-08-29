import sympy
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

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys 'G', 'X', 'action', 'x',
    or a tuple (G, X, action, x).
    """
    if isinstance(witness, dict):
        G = witness.get('G')
        X = witness.get('X')
        action = witness.get('action')
        x = witness.get('x')
    elif isinstance(witness, (list, tuple)) and len(witness) == 4:
        G, X, action, x = witness
    else:
        return [False, False, False, False]

    try:
        X = list(X)
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        if hasattr(G, 'is_group') and G.is_group:
            order = G.order()
            h1 = (order > 0 and order < float('inf'))
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: G acts on X
    try:
        elements = list(G.elements)
        e = next(g for g in elements if g.is_Identity)
        
        h2 = True
        # Check identity and closure
        for y in X:
            if callable(action):
                ey = action(e, y)
            else:
                if (e, y) not in action:
                    h2 = False
                    break
                ey = action[(e, y)]
            
            if ey != y:
                h2 = False
                break
                
        if h2:
            for g in elements:
                for y in X:
                    if callable(action):
                        gy = action(g, y)
                    else:
                        if (g, y) not in action:
                            h2 = False
                            break
                        gy = action[(g, y)]
                    
                    if gy not in X:
                        h2 = False
                        break
                if not h2: break

        # Check compatibility (allowing both left and right actions to accommodate multiplication conventions)
        if h2:
            is_left = True
            is_right = True
            for g in elements:
                for h in elements:
                    gh = g * h
                    for y in X:
                        if callable(action):
                            hy = action(h, y)
                            g_hy = action(g, hy)
                            gy = action(g, y)
                            h_gy = action(h, gy)
                            gh_y = action(gh, y)
                        else:
                            hy = action[(h, y)]
                            g_hy = action[(g, hy)]
                            gy = action[(g, y)]
                            h_gy = action[(h, gy)]
                            gh_y = action[(gh, y)]
                        
                        if g_hy != gh_y:
                            is_left = False
                        if h_gy != gh_y:
                            is_right = False
                    if not is_left and not is_right:
                        break
                if not is_left and not is_right:
                    break
            if not is_left and not is_right:
                h2 = False
    except Exception:
        h2 = False

    # H_3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # ¬Q: The cardinality of the orbit of x does not divide the order of the group |G|
    try:
        elements = list(G.elements)
        orbit = []
        for g in elements:
            if callable(action):
                res = action(g, x)
            else:
                res = action[(g, x)]
            if res not in orbit:
                orbit.append(res)
        orbit_size = len(orbit)
        group_order = G.order()
        
        neg_q = (group_order % orbit_size != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G acts on X",
    "H_3: x is an element of X",
    "¬Q: The cardinality of the orbit of x does not divide the order of the group |G|"
]

N_HYP = 3
NEG_Q_INDEX = 3