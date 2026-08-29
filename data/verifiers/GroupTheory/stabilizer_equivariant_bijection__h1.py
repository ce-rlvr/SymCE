import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

CONDITION_LABELS = [
    "H_1: X and Y are sets equipped with actions by G",
    "H_2: phi: X -> Y is a bijection such that phi(g * x) = g * phi(x) for all g in G and x in X",
    "H_3: x is an element of X",
    "¬Q: The point stabilizer G_x is not equal to the point stabilizer G_phi(x)"
]
N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness['G']
            G_op = witness.get('G_op')
            X = list(witness['X'])
            Y = list(witness['Y'])
            action_X = witness['action_X']
            action_Y = witness['action_Y']
            phi = witness['phi']
            x_elem = witness['x']
        else:
            G = witness.G
            G_op = getattr(witness, 'G_op', None)
            X = list(witness.X)
            Y = list(witness.Y)
            action_X = witness.action_X
            action_Y = witness.action_Y
            phi = witness.phi
            x_elem = witness.x
            
        if hasattr(G, 'elements'):
            G_elements = list(G.elements)
            G_op = lambda a, b: a * b
            identity = G.identity
            is_sympy_group = True
        else:
            G_elements = list(G)
            is_sympy_group = False
            identity = None
            for e in G_elements:
                if all(G_op(e, g) == g and G_op(g, e) == g for g in G_elements):
                    identity = e
                    break
    except Exception:
        return [False, False, False, False]

    h1_ok = True
    try:
        if not is_sympy_group:
            if identity is None:
                h1_ok = False
            else:
                for g1 in G_elements:
                    for g2 in G_elements:
                        if G_op(g1, g2) not in G_elements:
                            h1_ok = False
                            break
                    if not h1_ok: break
                if h1_ok:
                    for g in G_elements:
                        has_inv = False
                        for inv in G_elements:
                            if G_op(g, inv) == identity and G_op(inv, g) == identity:
                                has_inv = True
                                break
                        if not has_inv:
                            h1_ok = False
                            break
        
        if h1_ok:
            for g in G_elements:
                for x in X:
                    if action_X(g, x) not in X:
                        h1_ok = False
            for x in X:
                if action_X(identity, x) != x:
                    h1_ok = False
            for g1 in G_elements:
                for g2 in G_elements:
                    for x in X:
                        if action_X(g1, action_X(g2, x)) != action_X(G_op(g1, g2), x):
                            h1_ok = False
                            
            for g in G_elements:
                for y in Y:
                    if action_Y(g, y) not in Y:
                        h1_ok = False
            for y in Y:
                if action_Y(identity, y) != y:
                    h1_ok = False
            for g1 in G_elements:
                for g2 in G_elements:
                    for y in Y:
                        if action_Y(g1, action_Y(g2, y)) != action_Y(G_op(g1, g2), y):
                            h1_ok = False
    except Exception:
        h1_ok = False

    h2_ok = True
    try:
        phi_X = []
        for x in X:
            y = phi(x)
            if y not in Y:
                h2_ok = False
            phi_X.append(y)
            
        if h2_ok:
            if len(X) != len(Y):
                h2_ok = False
            else:
                for y in Y:
                    if y not in phi_X:
                        h2_ok = False
                        break
                if h2_ok:
                    for i in range(len(X)):
                        for j in range(i+1, len(X)):
                            if phi_X[i] == phi_X[j] and X[i] != X[j]:
                                h2_ok = False
                                break
                        if not h2_ok: break
                        
        if h2_ok:
            for g in G_elements:
                for x in X:
                    if phi(action_X(g, x)) != action_Y(g, phi(x)):
                        h2_ok = False
                        break
                if not h2_ok: break
    except Exception:
        h2_ok = False

    h3_ok = True
    try:
        if x_elem not in X:
            h3_ok = False
    except Exception:
        h3_ok = False

    neg_q_ok = False
    try:
        G_x = []
        for g in G_elements:
            if action_X(g, x_elem) == x_elem:
                G_x.append(g)
                
        phi_x = phi(x_elem)
        G_phi_x = []
        for g in G_elements:
            if action_Y(g, phi_x) == phi_x:
                G_phi_x.append(g)
                
        def is_equal(list1, list2):
            if len(list1) != len(list2): return False
            for item in list1:
                if item not in list2: return False
            for item in list2:
                if item not in list1: return False
            return True
            
        neg_q_ok = not is_equal(G_x, G_phi_x)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]