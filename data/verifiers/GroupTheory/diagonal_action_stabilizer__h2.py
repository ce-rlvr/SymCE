import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math
import z3

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        G = witness['G']
        X = witness['X']
        Y = witness['Y']
        action_X = witness['action_X']
        action_Y = witness['action_Y']
        action_XY = witness['action_XY']
        x_val = witness['x']
        y_val = witness['y']
    except (KeyError, TypeError):
        return [False, False, False]

    # Extract elements and find identity
    try:
        if hasattr(G, 'elements'):
            elements = list(G.elements)
            id_elem = G.identity
        else:
            elements = list(G)
            id_elem = None
            for e in elements:
                if all(e * g == g for g in elements):
                    id_elem = e
                    break
    except Exception:
        return [False, False, False]

    # H_1: G is a group acting on a set X and a set Y (and X x Y)
    try:
        h1_ok = True
        if id_elem is None:
            h1_ok = False
        
        # Check group axioms
        if h1_ok:
            for g1 in elements:
                for g2 in elements:
                    if not any(g1 * g2 == e for e in elements):
                        h1_ok = False
                has_inv = False
                for g2 in elements:
                    if g1 * g2 == id_elem and g2 * g1 == id_elem:
                        has_inv = True
                        break
                if not has_inv:
                    h1_ok = False
                    
        # Check action on X
        if h1_ok:
            for x in X:
                if action_X(id_elem, x) != x: 
                    h1_ok = False
                for g1 in elements:
                    res1 = action_X(g1, x)
                    if not any(res1 == e for e in X): 
                        h1_ok = False
                    for g2 in elements:
                        if action_X(g1, action_X(g2, x)) != action_X(g1 * g2, x):
                            h1_ok = False
                            
        # Check action on Y
        if h1_ok:
            for y in Y:
                if action_Y(id_elem, y) != y: 
                    h1_ok = False
                for g1 in elements:
                    res1 = action_Y(g1, y)
                    if not any(res1 == e for e in Y): 
                        h1_ok = False
                    for g2 in elements:
                        if action_Y(g1, action_Y(g2, y)) != action_Y(g1 * g2, y):
                            h1_ok = False
                            
        # Check action on X x Y
        if h1_ok:
            XY = [(x, y) for x in X for y in Y]
            for xy in XY:
                if action_XY(id_elem, xy) != xy: 
                    h1_ok = False
                for g1 in elements:
                    res1 = action_XY(g1, xy)
                    if not any(res1 == e for e in XY): 
                        h1_ok = False
                    for g2 in elements:
                        if action_XY(g1, action_XY(g2, xy)) != action_XY(g1 * g2, xy):
                            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: x in X and y in Y
    try:
        h2_ok = any(x_val == e for e in X) and any(y_val == e for e in Y)
    except Exception:
        h2_ok = False

    # ¬Q: The stabilizer subgroup G_{(x, y)} is not equal to the intersection G_x \cap G_y
    try:
        G_x = [g for g in elements if action_X(g, x_val) == x_val]
        G_y = [g for g in elements if action_Y(g, y_val) == y_val]
        G_x_cap_y = [g for g in G_x if any(g == e for e in G_y)]
        
        G_xy = [g for g in elements if action_XY(g, (x_val, y_val)) == (x_val, y_val)]
        
        def is_subset(l1, l2):
            return all(any(e1 == e2 for e2 in l2) for e1 in l1)
            
        neg_q = not (is_subset(G_xy, G_x_cap_y) and is_subset(G_x_cap_y, G_xy))
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X and a set Y",
    "H_2: x in X and y in Y",
    "¬Q: The stabilizer subgroup G_{(x, y)} is not equal to the intersection G_x \\cap G_y"
]

N_HYP = 2
NEG_Q_INDEX = 2