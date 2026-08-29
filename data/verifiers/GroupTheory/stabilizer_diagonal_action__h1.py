import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        G = list(witness['G'])
        X = list(witness['X'])
        Y = list(witness['Y'])
        action_X = witness['action_X']
        action_Y = witness['action_Y']
        x = witness['x']
        y = witness['y']
        
        # H_1: X and Y are sets on which G acts
        h1 = True
        for g in G:
            for xi in X:
                if action_X(g, xi) not in X:
                    h1 = False
            for yi in Y:
                if action_Y(g, yi) not in Y:
                    h1 = False
                    
        # H_2: G acts on X \times Y via the diagonal action
        action_XY = witness.get('action_XY')
        if action_XY is not None:
            h2 = True
            for g in G:
                for xi in X:
                    for yi in Y:
                        if action_XY(g, (xi, yi)) != (action_X(g, xi), action_Y(g, yi)):
                            h2 = False
        else:
            h2 = True
            action_XY = lambda g, xy: (action_X(g, xy[0]), action_Y(g, xy[1]))
            
        # H_3: (x, y) is an element of X \times Y
        h3 = (x in X) and (y in Y)
        
        # Conclusion: The stabilizer of (x, y) in G is the intersection of the stabilizers G_x and G_y.
        G_x = [g for g in G if action_X(g, x) == x]
        G_y = [g for g in G if action_Y(g, y) == y]
        intersection = [g for g in G if g in G_x and g in G_y]
        
        stab_xy = [g for g in G if action_XY(g, (x, y)) == (x, y)]
        
        q = True
        for g in G:
            in_stab = (g in stab_xy)
            in_int = (g in intersection)
            if in_stab != in_int:
                q = False
                break
                
        neg_q = not q
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: X and Y are sets on which G acts",
    "H_2: G acts on X \\times Y via the diagonal action",
    "H_3: (x, y) is an element of X \\times Y",
    "¬Q: The stabilizer of (x, y) in G is not the intersection of the stabilizers G_x and G_y"
]

N_HYP = 3
NEG_Q_INDEX = 3