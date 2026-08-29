import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup
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
    """
    witness is expected to be a dictionary with keys:
    'G': list of elements or a PermutationGroup
    'X': list of elements in set X
    'Y': list of elements in set Y
    'action_X': callable f(g, x) or dict {(g, x): x_new} (defaults to g(x) if None)
    'action_Y': callable f(g, y) or dict {(g, y): y_new} (defaults to g(y) if None)
    'action_XY': callable f(g, (x, y)) or dict {(g, (x, y)): (x_new, y_new)}
    'x': element x
    'y': element y
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G', [])
            X = witness.get('X', [])
            Y = witness.get('Y', [])
            action_X = witness.get('action_X', None)
            action_Y = witness.get('action_Y', None)
            action_XY = witness.get('action_XY', None)
            x = witness.get('x', None)
            y = witness.get('y', None)
        elif isinstance(witness, (list, tuple)):
            G = witness[0]
            X = witness[1]
            Y = witness[2]
            action_X = witness[3] if len(witness) > 3 else None
            action_Y = witness[4] if len(witness) > 4 else None
            action_XY = witness[5] if len(witness) > 5 else None
            x = witness[6] if len(witness) > 6 else None
            y = witness[7] if len(witness) > 7 else None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        elif hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        if hasattr(G, 'is_group') and G.is_group:
            h1 = True
            e = G.identity
        else:
            e = None
            for g in elements:
                if all(g * h == h for h in elements) and all(h * g == h for h in elements):
                    e = g
                    break
            if e is None:
                h1 = False
            else:
                h1 = True
                for g in elements:
                    for h in elements:
                        if (g * h) not in elements:
                            h1 = False
    except Exception:
        h1 = False

    # H2: X and Y are sets on which G acts
    try:
        def act_X(g, elem):
            if action_X is None: return g(elem)
            if callable(action_X): return action_X(g, elem)
            return action_X[(g, elem)]
            
        def act_Y(g, elem):
            if action_Y is None: return g(elem)
            if callable(action_Y): return action_Y(g, elem)
            return action_Y[(g, elem)]

        h2 = True
        for elem in X:
            if act_X(e, elem) != elem:
                h2 = False
        for elem in Y:
            if act_Y(e, elem) != elem:
                h2 = False
                
        left_ok = True
        right_ok = True
        for g in elements:
            for h in elements:
                gh = g * h
                for elem in X:
                    if act_X(g, act_X(h, elem)) != act_X(gh, elem):
                        left_ok = False
                    if act_X(h, act_X(g, elem)) != act_X(gh, elem):
                        right_ok = False
                for elem in Y:
                    if act_Y(g, act_Y(h, elem)) != act_Y(gh, elem):
                        left_ok = False
                    if act_Y(h, act_Y(g, elem)) != act_Y(gh, elem):
                        right_ok = False
                        
        if not (left_ok or right_ok):
            h2 = False
    except Exception:
        h2 = False

    # H3: G acts on X \times Y via the diagonal action
    try:
        def act_XY(g, elem):
            if action_XY is None: return (act_X(g, elem[0]), act_Y(g, elem[1]))
            if callable(action_XY): return action_XY(g, elem)
            return action_XY[(g, elem)]

        h3 = True
        for x_elem in X:
            for y_elem in Y:
                if act_XY(e, (x_elem, y_elem)) != (x_elem, y_elem):
                    h3 = False
        
        left_xy_ok = True
        right_xy_ok = True
        for g in elements:
            for h in elements:
                gh = g * h
                for x_elem in X:
                    for y_elem in Y:
                        if act_XY(g, act_XY(h, (x_elem, y_elem))) != act_XY(gh, (x_elem, y_elem)):
                            left_xy_ok = False
                        if act_XY(h, act_XY(g, (x_elem, y_elem))) != act_XY(gh, (x_elem, y_elem)):
                            right_xy_ok = False
                            
        if not (left_xy_ok or right_xy_ok):
            h3 = False

        for g in elements:
            for x_elem in X:
                for y_elem in Y:
                    if act_XY(g, (x_elem, y_elem)) != (act_X(g, x_elem), act_Y(g, y_elem)):
                        h3 = False
    except Exception:
        h3 = False

    # ¬Q: The stabilizer of (x, y) in G is not the intersection of the stabilizers G_x and G_y
    try:
        stab_xy = []
        for g in elements:
            if act_XY(g, (x, y)) == (x, y):
                if g not in stab_xy: stab_xy.append(g)
                
        stab_x = []
        for g in elements:
            if act_X(g, x) == x:
                if g not in stab_x: stab_x.append(g)
                
        stab_y = []
        for g in elements:
            if act_Y(g, y) == y:
                if g not in stab_y: stab_y.append(g)
                
        intersection = [g for g in stab_x if g in stab_y]
        
        neg_q = False
        for g in stab_xy:
            if g not in intersection:
                neg_q = True
        for g in intersection:
            if g not in stab_xy:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X and Y are sets on which G acts",
    "H_3: G acts on X \\times Y via the diagonal action",
    "¬Q: The stabilizer of (x, y) in G is not the intersection of the stabilizers G_x and G_y"
]

N_HYP = 3
NEG_Q_INDEX = 3