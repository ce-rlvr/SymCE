import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def apply2(f, a, b):
    if isinstance(f, dict):
        return f[(a, b)]
    return f(a, b)

def is_group(elements, op, identity):
    if identity not in elements: 
        return False
    for a in elements:
        if apply2(op, identity, a) != a or apply2(op, a, identity) != a: 
            return False
        has_inv = False
        for b in elements:
            if apply2(op, a, b) == identity and apply2(op, b, a) == identity:
                has_inv = True
                break
        if not has_inv: 
            return False
        for b in elements:
            ab = apply2(op, a, b)
            if ab not in elements: 
                return False
            for c in elements:
                bc = apply2(op, b, c)
                if apply2(op, ab, c) != apply2(op, a, bc): 
                    return False
    return True

def is_action(group, op, identity, space, action):
    for s in space:
        if apply2(action, identity, s) != s: 
            return False
    for g1 in group:
        for g2 in group:
            g1g2 = apply2(op, g1, g2)
            for s in space:
                g2s = apply2(action, g2, s)
                if apply2(action, g1g2, s) != apply2(action, g1, g2s): 
                    return False
                if apply2(action, g1, s) not in space: 
                    return False
    return True

def check_h1(witness):
    H = witness['H']
    op_H = witness['op_H']
    id_H = witness['id_H']
    Y = list(witness['Y'])
    action_H = witness['action_H']
    
    if not is_group(H, op_H, id_H): 
        return False
    if not is_action(H, op_H, id_H, Y, action_H): 
        return False
    return True

def check_h2(witness):
    G = witness['G']
    op_G = witness['op_G']
    id_G = witness['id_G']
    
    H = witness['H']
    op_H = witness['op_H']
    id_H = witness['id_H']
    
    X = list(witness['X'])
    Y = list(witness['Y'])
    
    action_GH = witness['action_GH']
    
    if not is_group(G, op_G, id_G): 
        return False
    if not is_group(H, op_H, id_H): 
        return False
    
    GH = [(g, h) for g in G for h in H]
    id_GH = (id_G, id_H)
    def op_GH(gh1, gh2):
        return (apply2(op_G, gh1[0], gh2[0]), apply2(op_H, gh1[1], gh2[1]))
        
    XY = [(x_elem, y_elem) for x_elem in X for y_elem in Y]
    
    if not is_action(GH, op_GH, id_GH, XY, action_GH): 
        return False
    
    if X and Y:
        x0 = X[0]
        y0 = Y[0]
        for g in G:
            for h in H:
                for x_elem in X:
                    for y_elem in Y:
                        res = apply2(action_GH, (g, h), (x_elem, y_elem))
                        expected_0 = apply2(action_GH, (g, id_H), (x_elem, y0))[0]
                        expected_1 = apply2(action_GH, (id_G, h), (x0, y_elem))[1]
                        if res != (expected_0, expected_1):
                            return False
    return True

def check_h3(witness):
    X = list(witness['X'])
    Y = list(witness['Y'])
    x = witness['x']
    y = witness['y']
    return (x in X) and (y in Y)

def check_neg_q(witness):
    G = witness['G']
    H = witness['H']
    id_H = witness['id_H']
    x = witness['x']
    y = witness['y']
    action_H = witness['action_H']
    action_GH = witness['action_GH']
    
    Stab_GxH = set()
    for g in G:
        for h in H:
            if apply2(action_GH, (g, h), (x, y)) == (x, y):
                Stab_GxH.add((g, h))
                
    Stab_G = set()
    if 'action_G' in witness:
        action_G = witness['action_G']
        for g in G:
            if apply2(action_G, g, x) == x:
                Stab_G.add(g)
    else:
        for g in G:
            if apply2(action_GH, (g, id_H), (x, y))[0] == x:
                Stab_G.add(g)
            
    Stab_H = set()
    for h in H:
        if apply2(action_H, h, y) == y:
            Stab_H.add(h)
            
    expected_Stab = set((g, h) for g in Stab_G for h in Stab_H)
    
    return Stab_GxH != expected_Stab

def conditions(witness):
    try:
        h1 = bool(check_h1(witness))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(check_h2(witness))
    except Exception:
        h2 = False
        
    try:
        h3 = bool(check_h3(witness))
    except Exception:
        h3 = False
        
    try:
        neg_q = bool(check_neg_q(witness))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group acting on a set Y",
    "H_2: The direct product G \\times H acts on the Cartesian product X \\times Y componentwise",
    "H_3: (x, y) is an element of X \\times Y",
    "¬Q: The stabilizer of (x, y) in G \\times H is not the direct product of the stabilizer of x in G and the stabilizer of y in H"
]

N_HYP = 3
NEG_Q_INDEX = 3