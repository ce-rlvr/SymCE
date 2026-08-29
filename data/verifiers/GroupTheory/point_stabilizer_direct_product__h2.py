import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_group(G, op):
    if not G: 
        return False, None
    G_list = list(G)
    for a in G_list:
        for b in G_list:
            try:
                if op(a, b) not in G_list: 
                    return False, None
            except Exception:
                return False, None
    for a in G_list:
        for b in G_list:
            for c in G_list:
                if op(a, op(b, c)) != op(op(a, b), c): 
                    return False, None
    for e in G_list:
        if all(op(e, a) == a and op(a, e) == a for a in G_list):
            inv_ok = True
            for a in G_list:
                if not any(op(a, b) == e and op(b, a) == e for b in G_list):
                    inv_ok = False
                    break
            if inv_ok:
                return True, e
    return False, None

def is_action(G, X, op, action, e):
    X_list = list(X)
    if not X_list: 
        return False
    for x in X_list:
        if action(e, x) != x: 
            return False
    for g1 in G:
        for g2 in G:
            for x in X_list:
                if action(g1, action(g2, x)) != action(op(g1, g2), x): 
                    return False
    return True

def is_action_GH(G, H, X, Y, op_G, op_H, action_GH, e_G, e_H):
    X_list = list(X)
    Y_list = list(Y)
    for x in X_list:
        for y in Y_list:
            if tuple(action_GH(e_G, e_H, x, y)) != (x, y): 
                return False
    for g1 in G:
        for h1 in H:
            for g2 in G:
                for h2 in H:
                    for x in X_list:
                        for y in Y_list:
                            res1 = tuple(action_GH(g2, h2, x, y))
                            if res1[0] not in X_list or res1[1] not in Y_list: 
                                return False
                            res2 = tuple(action_GH(g1, h1, res1[0], res1[1]))
                            res3 = tuple(action_GH(op_G(g1, g2), op_H(h1, h2), x, y))
                            if res2 != res3: 
                                return False
    return True

def conditions(witness):
    try:
        G = list(witness['G'])
        H = list(witness['H'])
        X = list(witness['X'])
        Y = list(witness['Y'])
        op_G = witness['op_G']
        op_H = witness['op_H']
        action_G = witness['action_G']
        action_H = witness['action_H']
        raw_action_GH = witness['action_GH']
        x = witness['x']
        y = witness['y']
        
        try:
            raw_action_GH(G[0], H[0], X[0], Y[0])
            action_GH = raw_action_GH
        except TypeError:
            action_GH = lambda g, h, px, py: raw_action_GH((g, h), (px, py))
            
    except Exception:
        return [False, False, False]
        
    # H_1: G and H are groups acting on sets X and Y respectively
    try:
        ok_G, e_G = is_group(G, op_G)
        ok_H, e_H = is_group(H, op_H)
        
        if ok_G and ok_H:
            act_G_ok = is_action(G, X, op_G, action_G, e_G)
            act_H_ok = is_action(H, Y, op_H, action_H, e_H)
            act_GH_ok = is_action_GH(G, H, X, Y, op_G, op_H, action_GH, e_G, e_H)
            h1 = act_G_ok and act_H_ok and act_GH_ok
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: x in X and y in Y
    try:
        h2 = (x in X) and (y in Y)
    except Exception:
        h2 = False
        
    # ¬Q: The stabilizer of the pair (x, y) in G × H is NOT exactly Stab_G(x) × Stab_H(y)
    try:
        stab_G = [g for g in G if action_G(g, x) == x]
        stab_H = [h for h in H if action_H(h, y) == y]
        
        stab_prod = set((g, h) for g in stab_G for h in stab_H)
        
        stab_GH = set()
        for g in G:
            for h in H:
                if tuple(action_GH(g, h, x, y)) == (x, y):
                    stab_GH.add((g, h))
                    
        neg_q = (stab_prod != stab_GH)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups acting on sets X and Y respectively",
    "H_2: x in X and y in Y",
    "¬Q: The stabilizer of the pair (x, y) in G × H is NOT exactly Stab_G(x) × Stab_H(y)"
]

N_HYP = 2
NEG_Q_INDEX = 2