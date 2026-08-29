import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: The direct product group G × H acts on the Cartesian product X × Y via (g, h) · (x, y) = (g · x, h · y)",
    "H_2: x ∈ X and y ∈ Y",
    "¬Q: The stabilizer of the pair (x, y) in G × H is not exactly the direct product of the individual stabilizers Stab_G(x) × Stab_H(y)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_group(elements, op):
    if not elements: return False, None
    for a in elements:
        for b in elements:
            try:
                if op(a, b) not in elements:
                    return False, None
            except Exception:
                return False, None
    for a in elements:
        for b in elements:
            for c in elements:
                try:
                    if op(op(a, b), c) != op(a, op(b, c)):
                        return False, None
                except Exception:
                    return False, None
    identity = None
    for e in elements:
        try:
            if all(op(e, a) == a and op(a, e) == a for a in elements):
                identity = e
                break
        except Exception:
            pass
    if identity is None:
        return False, None
    for a in elements:
        has_inv = False
        for b in elements:
            try:
                if op(a, b) == identity and op(b, a) == identity:
                    has_inv = True
                    break
            except Exception:
                pass
        if not has_inv:
            return False, None
    return True, identity

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        H = witness['H']
        X = witness['X']
        Y = witness['Y']
        op_G = witness['op_G']
        op_H = witness['op_H']
        action_G = witness['action_G']
        action_H = witness['action_H']
        x_val = witness['x']
        y_val = witness['y']
    except (TypeError, KeyError):
        return [False, False, False]

    h1_ok = False
    try:
        g_is_group, e_G = is_group(G, op_G)
        h_is_group, e_H = is_group(H, op_H)
        
        if g_is_group and h_is_group:
            action_GxH = witness.get('action_GxH')
            formula_holds = True
            if action_GxH:
                for g in G:
                    for h in H:
                        for xi in X:
                            for yi in Y:
                                if action_GxH((g, h), (xi, yi)) != (action_G(g, xi), action_H(h, yi)):
                                    formula_holds = False
                                    break
                            if not formula_holds: break
                        if not formula_holds: break
                    if not formula_holds: break
            
            if formula_holds:
                id_acts_trivially = True
                for xi in X:
                    for yi in Y:
                        if action_G(e_G, xi) != xi or action_H(e_H, yi) != yi:
                            id_acts_trivially = False
                            break
                    if not id_acts_trivially:
                        break
                
                if id_acts_trivially:
                    compatible = True
                    for g1 in G:
                        for h1 in H:
                            for g2 in G:
                                for h2 in H:
                                    g1g2 = op_G(g1, g2)
                                    h1h2 = op_H(h1, h2)
                                    for xi in X:
                                        for yi in Y:
                                            act1_x = action_G(g1g2, xi)
                                            act1_y = action_H(h1h2, yi)
                                            
                                            act2_x = action_G(g1, action_G(g2, xi))
                                            act2_y = action_H(h1, action_H(h2, yi))
                                            
                                            if act1_x != act2_x or act1_y != act2_y:
                                                compatible = False
                                                break
                                        if not compatible: break
                                    if not compatible: break
                                if not compatible: break
                            if not compatible: break
                    if compatible:
                        h1_ok = True
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        if x_val in X and y_val in Y:
            h2_ok = True
    except Exception:
        h2_ok = False

    neg_q_ok = False
    try:
        action_GxH = witness.get('action_GxH')
        
        stab_GxH = []
        for g in G:
            for h in H:
                if action_GxH:
                    res = action_GxH((g, h), (x_val, y_val))
                    if res == (x_val, y_val):
                        stab_GxH.append((g, h))
                else:
                    if action_G(g, x_val) == x_val and action_H(h, y_val) == y_val:
                        stab_GxH.append((g, h))
        
        stab_G = [g for g in G if action_G(g, x_val) == x_val]
        stab_H = [h for h in H if action_H(h, y_val) == y_val]
        
        dir_prod_stabs = []
        for g in stab_G:
            for h in stab_H:
                dir_prod_stabs.append((g, h))
                
        stab_G_is_group, _ = is_group(stab_G, op_G)
        stab_H_is_group, _ = is_group(stab_H, op_H)
        
        sets_equal = True
        if len(stab_GxH) != len(dir_prod_stabs):
            sets_equal = False
        else:
            for elem in stab_GxH:
                if elem not in dir_prod_stabs:
                    sets_equal = False
                    break
            if sets_equal:
                for elem in dir_prod_stabs:
                    if elem not in stab_GxH:
                        sets_equal = False
                        break
                        
        if not sets_equal or not stab_G_is_group or not stab_H_is_group:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]