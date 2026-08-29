import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(elements, op):
    elements = list(elements)
    if not elements: return False
    for a in elements:
        for b in elements:
            try:
                if op(a, b) not in elements: return False
            except Exception:
                return False
    for a in elements:
        for b in elements:
            for c in elements:
                try:
                    if op(op(a, b), c) != op(a, op(b, c)): return False
                except Exception:
                    return False
    identity = None
    for e in elements:
        is_id = True
        for a in elements:
            try:
                if op(e, a) != a or op(a, e) != a:
                    is_id = False
                    break
            except Exception:
                is_id = False
                break
        if is_id:
            identity = e
            break
    if identity is None: return False
    for a in elements:
        has_inv = False
        for b in elements:
            try:
                if op(a, b) == identity and op(b, a) == identity:
                    has_inv = True
                    break
            except Exception:
                pass
        if not has_inv: return False
    return True

def is_action(G, X, op_G, action):
    G = list(G)
    X = list(X)
    if not X: return True
    identity = None
    for e in G:
        is_id = True
        for a in G:
            try:
                if op_G(e, a) != a or op_G(a, e) != a:
                    is_id = False
                    break
            except Exception:
                is_id = False
                break
        if is_id:
            identity = e
            break
    if identity is None: return False
    
    for x in X:
        try:
            if action(identity, x) != x: return False
        except Exception:
            return False
            
    for g1 in G:
        for g2 in G:
            for x in X:
                try:
                    if action(op_G(g1, g2), x) != action(g1, action(g2, x)):
                        return False
                except Exception:
                    return False
                    
    for g in G:
        for x in X:
            try:
                if action(g, x) not in X: return False
            except Exception:
                return False
                
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = list(witness['G'])
            H = list(witness['H'])
            X = list(witness['X'])
            Y = list(witness['Y'])
            op_G = witness['op_G']
            op_H = witness['op_H']
            action_G = witness['action_G']
            action_H = witness['action_H']
            action_GH = witness['action_GH']
            x_val = witness['x']
            y_val = witness['y']
        else:
            G = list(witness.G)
            H = list(witness.H)
            X = list(witness.X)
            Y = list(witness.Y)
            op_G = witness.op_G
            op_H = witness.op_H
            action_G = witness.action_G
            action_H = witness.action_H
            action_GH = witness.action_GH
            x_val = witness.x
            y_val = witness.y
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(is_group(G, op_G) and 
                     is_group(H, op_H) and 
                     is_action(G, X, op_G, action_G) and 
                     is_action(H, Y, op_H, action_H))
    except Exception:
        h1_ok = False

    try:
        h2_ok = True
        for g in G:
            for h in H:
                for x in X:
                    for y in Y:
                        if action_GH((g, h), (x, y)) != (action_G(g, x), action_H(h, y)):
                            h2_ok = False
                            break
                    if not h2_ok: break
                if not h2_ok: break
            if not h2_ok: break
            
        if h2_ok:
            GxH = [(g, h) for g in G for h in H]
            XxY = [(x, y) for x in X for y in Y]
            def op_GH(gh1, gh2):
                return (op_G(gh1[0], gh2[0]), op_H(gh1[1], gh2[1]))
            if not is_action(GxH, XxY, op_GH, action_GH):
                h2_ok = False
    except Exception:
        h2_ok = False

    try:
        stab_G = [g for g in G if action_G(g, x_val) == x_val]
        stab_H = [h for h in H if action_H(h, y_val) == y_val]
        stab_G_x_stab_H = [(g, h) for g in stab_G for h in stab_H]
        
        GxH = [(g, h) for g in G for h in H]
        stab_GH = [gh for gh in GxH if action_GH(gh, (x_val, y_val)) == (x_val, y_val)]
        
        def is_subset(list1, list2):
            for item in list1:
                if item not in list2:
                    return False
            return True
            
        same_elements = is_subset(stab_GH, stab_G_x_stab_H) and is_subset(stab_G_x_stab_H, stab_GH)
        neg_q_ok = not same_elements
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups acting on sets X and Y respectively",
    "H_2: The direct product group G × H acts on the Cartesian product X × Y via (g, h) · (x, y) = (g · x, h · y)",
    "¬Q: The stabilizer of (x, y) in G × H is NOT exactly Stab_G(x) × Stab_H(y)"
]

N_HYP = 2
NEG_Q_INDEX = 2