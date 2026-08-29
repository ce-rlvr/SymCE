import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Standard bindings
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

CONDITION_LABELS = [
    "H_1: G acts on X x Y via the diagonal action",
    "H_2: x in X and y in Y",
    "¬Q: The stabilizer subgroup G_{(x, y)} is not equal to the intersection G_x \\cap G_y (e.g. it is not a subgroup)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G = list(witness.G)
        X = list(witness.X)
        Y = list(witness.Y)
        x = witness.x
        y = witness.y
        
        op = witness.op if hasattr(witness, 'op') else lambda a, b: a * b
        
        if hasattr(witness, 'action_X') and hasattr(witness, 'action_Y'):
            action_X = witness.action_X
            action_Y = witness.action_Y
            if hasattr(witness, 'action'):
                action = witness.action
            else:
                action = lambda g, pt: (action_X(g, pt[0]), action_Y(g, pt[1]))
        elif hasattr(witness, 'action'):
            action = witness.action
            action_X = lambda g, x_val: action(g, (x_val, Y[0]))[0]
            action_Y = lambda g, y_val: action(g, (X[0], y_val))[1]
        else:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    # H1: G acts on X x Y via the diagonal action
    h1 = True
    try:
        for g in G:
            for x_val in X:
                for y_val in Y:
                    pt = (x_val, y_val)
                    res = action(g, pt)
                    if res != (action_X(g, x_val), action_Y(g, y_val)):
                        h1 = False
                        break
                if not h1: break
            if not h1: break
            
        # Check compatibility (action axioms)
        for g1 in G:
            for g2 in G:
                g1g2 = op(g1, g2)
                for x_val in X:
                    if action_X(g1, action_X(g2, x_val)) != action_X(g1g2, x_val):
                        h1 = False
                for y_val in Y:
                    if action_Y(g1, action_Y(g2, y_val)) != action_Y(g1g2, y_val):
                        h1 = False
    except Exception:
        h1 = False

    # H2: x in X and y in Y
    h2 = False
    try:
        h2 = (x in X) and (y in Y)
    except Exception:
        h2 = False

    # Conclusion: The stabilizer subgroup G_{(x, y)} is equal to the intersection G_x \cap G_y
    # Negation: G_{(x,y)} is NOT a subgroup OR G_{(x,y)} != G_x \cap G_y
    neg_q = False
    try:
        G_xy = [g for g in G if action(g, (x, y)) == (x, y)]
        G_x = [g for g in G if action_X(g, x) == x]
        G_y = [g for g in G if action_Y(g, y) == y]
        
        intersection = [g for g in G_x if g in G_y]
        
        sets_equal = (len(G_xy) == len(intersection)) and all(g in intersection for g in G_xy)
        
        # Check if G_xy is a subgroup of G
        identities = [e for e in G if all(op(e, g) == g and op(g, e) == g for g in G)]
        if not identities:
            is_subgroup = False
        else:
            e = identities[0]
            if e not in G_xy:
                is_subgroup = False
            else:
                is_subgroup = True
                for g1 in G_xy:
                    for g2 in G_xy:
                        if op(g1, g2) not in G_xy:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
                
                if is_subgroup:
                    for g1 in G_xy:
                        has_inv = False
                        for g2 in G_xy:
                            if op(g1, g2) == e and op(g2, g1) == e:
                                has_inv = True
                                break
                        if not has_inv:
                            is_subgroup = False
                            break
                            
        neg_q = not (sets_equal and is_subgroup)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]