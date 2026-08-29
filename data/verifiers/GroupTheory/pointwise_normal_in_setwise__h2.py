import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def apply_action(g, y, action=None):
    if action is not None:
        return action(g, y)
    if hasattr(g, '__call__'):
        return g(y)
    return g * y

def lists_equal(l1, l2):
    if len(l1) != len(l2): 
        return False
    for x in l1:
        if x not in l2: return False
    for x in l2:
        if x not in l1: return False
    return True

def conditions(witness) -> list[bool]:
    try:
        action = None
        if isinstance(witness, (tuple, list)) and len(witness) > 0 and callable(witness[-1]):
            action = witness[-1]
            witness = witness[:-1]
            
        if len(witness) == 5:
            G, X, Y, G_Y, G_pY = witness
        elif len(witness) == 3:
            G, X, Y = witness
            G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
            Y_list = list(Y)
            G_Y = []
            G_pY = []
            for g in G_elems:
                g_Y = []
                for y in Y_list:
                    g_Y.append(apply_action(g, y, action))
                if len(g_Y) == len(Y_list) and all(gy in Y_list for gy in g_Y):
                    G_Y.append(g)
                if all(apply_action(g, y, action) == y for y in Y_list):
                    G_pY.append(g)
        else:
            return [False, False, False, False]
            
        G_elems = list(G.elements) if hasattr(G, 'elements') else list(G)
        X_list = list(X)
        Y_list = list(Y)
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group acting on a set X
    try:
        h1 = hasattr(G, 'elements') or isinstance(G, (list, tuple, set))
        h1 = h1 and isinstance(X, (set, list, tuple))
        if h1 and len(G_elems) > 0 and len(X_list) > 0:
            _ = apply_action(G_elems[0], X_list[0], action)
    except Exception:
        h1 = False
        
    # H2: G_Y is the setwise stabilizer of Y in G
    try:
        expected_G_Y = []
        for g in G_elems:
            g_Y = []
            for y in Y_list:
                g_Y.append(apply_action(g, y, action))
            if len(g_Y) == len(Y_list) and all(gy in Y_list for gy in g_Y):
                expected_G_Y.append(g)
        G_Y_elems = list(G_Y.elements) if hasattr(G_Y, 'elements') else list(G_Y)
        h2 = lists_equal(expected_G_Y, G_Y_elems)
    except Exception:
        h2 = False
        
    # H3: G_{(Y)} is the pointwise stabilizer of Y in G
    try:
        expected_G_pY = []
        for g in G_elems:
            if all(apply_action(g, y, action) == y for y in Y_list):
                expected_G_pY.append(g)
        G_pY_elems = list(G_pY.elements) if hasattr(G_pY, 'elements') else list(G_pY)
        h3 = lists_equal(expected_G_pY, G_pY_elems)
    except Exception:
        h3 = False
        
    # Q: The pointwise stabilizer G_{(Y)} is a normal subgroup of the setwise stabilizer G_Y
    try:
        q = True
        
        # Check if G_Y is a valid group
        for g1 in G_Y_elems:
            try:
                g1_inv = g1**-1
            except Exception:
                try:
                    g1_inv = ~g1
                except Exception:
                    q = False
                    break
            if g1_inv not in G_Y_elems:
                q = False
                break
            for g2 in G_Y_elems:
                if (g1 * g2) not in G_Y_elems:
                    q = False
                    break
            if not q:
                break
                
        # Check if G_pY is a valid group
        if q:
            for h1 in G_pY_elems:
                try:
                    h1_inv = h1**-1
                except Exception:
                    try:
                        h1_inv = ~h1
                    except Exception:
                        q = False
                        break
                if h1_inv not in G_pY_elems:
                    q = False
                    break
                for h2 in G_pY_elems:
                    if (h1 * h2) not in G_pY_elems:
                        q = False
                        break
                if not q:
                    break
                    
        # Check if G_pY is a subgroup of G_Y
        if q:
            for h in G_pY_elems:
                if h not in G_Y_elems:
                    q = False
                    break
                    
        # Check normality
        if q:
            for g in G_Y_elems:
                try:
                    g_inv = g**-1
                except Exception:
                    g_inv = ~g
                for h in G_pY_elems:
                    conj = g * h * g_inv
                    if conj not in G_pY_elems:
                        q = False
                        break
                if not q:
                    break
    except Exception:
        q = False
        
    return [bool(h1), bool(h2), bool(h3), not bool(q)]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: G_Y is the setwise stabilizer of Y in G",
    "H_3: G_{(Y)} is the pointwise stabilizer of Y in G",
    "¬Q: The pointwise stabilizer G_{(Y)} is not a normal subgroup of the setwise stabilizer G_Y"
]

N_HYP = 3
NEG_Q_INDEX = 3