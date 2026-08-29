import itertools
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def is_group(elements, op, id_elem):
    if id_elem not in elements: return False
    for a in elements:
        if op(id_elem, a) != a or op(a, id_elem) != a: return False
        has_inv = False
        for b in elements:
            if op(a, b) == id_elem and op(b, a) == id_elem:
                has_inv = True
                break
        if not has_inv: return False
        for b in elements:
            if op(a, b) not in elements: return False
            for c in elements:
                if op(op(a, b), c) != op(a, op(b, c)): return False
    return True

def is_action(elements, op, id_elem, domain, action):
    for a in domain:
        if action(id_elem, a) != a: return False
    for g in elements:
        for a in domain:
            if action(g, a) not in domain: return False
    for g1 in elements:
        for g2 in elements:
            for a in domain:
                if action(g1, action(g2, a)) != action(op(g1, g2), a): return False
    return True

def conditions(witness):
    # H1: G is a group acting on a set X.
    try:
        G = witness['G']
        op_G = witness['op_G']
        id_G = witness['id_G']
        X = witness['X']
        action_G = witness['action_G']
        domain_G = witness.get('domain_G', X)
        
        H1 = False
        if is_group(G, op_G, id_G) and is_action(G, op_G, id_G, domain_G, action_G):
            H1 = True
            for x_elem in X:
                if x_elem not in domain_G:
                    H1 = False
                    break
                for g in G:
                    if action_G(g, x_elem) not in X:
                        H1 = False
                        break
    except Exception:
        H1 = False

    # H2: H is a group acting on a set Y.
    try:
        H = witness['H']
        op_H = witness['op_H']
        id_H = witness['id_H']
        Y = witness['Y']
        action_H = witness['action_H']
        domain_H = witness.get('domain_H', Y)
        
        H2 = False
        if is_group(H, op_H, id_H) and is_action(H, op_H, id_H, domain_H, action_H):
            H2 = True
            for y_elem in Y:
                if y_elem not in domain_H:
                    H2 = False
                    break
                for h in H:
                    if action_H(h, y_elem) not in Y:
                        H2 = False
                        break
    except Exception:
        H2 = False

    # H3: The direct product G \times H acts on the Cartesian product X \times Y componentwise.
    try:
        action_GxH = witness['action_GxH']
        domain_GxH = witness['domain_GxH']
        
        H3 = True
        for x_in in X:
            for y_in in Y:
                if (x_in, y_in) not in domain_GxH:
                    H3 = False
                    
        if (witness['x'], witness['y']) not in domain_GxH:
            H3 = False
            
        GxH = list(itertools.product(G, H))
        id_GxH = (id_G, id_H)
        def op_GxH(gh1, gh2):
            return (op_G(gh1[0], gh2[0]), op_H(gh1[1], gh2[1]))
            
        if not is_action(GxH, op_GxH, id_GxH, domain_GxH, action_GxH):
            H3 = False
            
        for g in G:
            for h in H:
                for x_in in X:
                    for y_in in Y:
                        if action_GxH((g, h), (x_in, y_in)) != (action_G(g, x_in), action_H(h, y_in)):
                            H3 = False
    except Exception:
        H3 = False

    # neg_Q: The stabilizer of (x, y) in G \times H is NOT the direct product of the stabilizer of x in G and the stabilizer of y in H.
    try:
        x = witness['x']
        y = witness['y']
        
        if x not in domain_G or y not in domain_H:
            neg_Q = False
        else:
            stab_G_x = [g for g in G if action_G(g, x) == x]
            stab_H_y = [h for h in H if action_H(h, y) == y]
            
            expected_stab = set(itertools.product(stab_G_x, stab_H_y))
            actual_stab = set(gh for gh in GxH if action_GxH(gh, (x, y)) == (x, y))
            
            neg_Q = (actual_stab != expected_stab)
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: H is a group acting on a set Y",
    "H_3: The direct product G x H acts on the Cartesian product X x Y componentwise",
    "¬Q: The stabilizer of (x, y) in G x H is not the direct product of the stabilizer of x in G and the stabilizer of y in H"
]

N_HYP = 3
NEG_Q_INDEX = 3