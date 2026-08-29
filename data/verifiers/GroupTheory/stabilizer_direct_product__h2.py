import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        G = witness['G']
        op_G = witness['op_G']
        id_G = witness['id_G']
        X = witness['X']
        action_G = witness['action_G']
        
        H = witness['H']
        op_H = witness['op_H']
        id_H = witness['id_H']
        Y = witness['Y']
        action_GH = witness['action_GH']
        
        x_w = witness['x']
        y_w = witness['y']
    except Exception:
        return [False, False, False, False]

    # H1: G is a group acting on a set X
    h1_ok = True
    try:
        if id_G not in G: h1_ok = False
        for g in G:
            if op_G(id_G, g) != g or op_G(g, id_G) != g: h1_ok = False
            has_inv = False
            for inv in G:
                if op_G(g, inv) == id_G and op_G(inv, g) == id_G:
                    has_inv = True
                    break
            if not has_inv: h1_ok = False
        for g1 in G:
            for g2 in G:
                if op_G(g1, g2) not in G: h1_ok = False
                for g3 in G:
                    if op_G(g1, op_G(g2, g3)) != op_G(op_G(g1, g2), g3): h1_ok = False
        
        for x in X:
            if action_G(id_G, x) != x: h1_ok = False
            for g1 in G:
                for g2 in G:
                    if action_G(g1, action_G(g2, x)) != action_G(op_G(g1, g2), x): h1_ok = False
                if action_G(g1, x) not in X: h1_ok = False
    except Exception:
        h1_ok = False

    # H2: The direct product G \times H acts on the Cartesian product X \times Y componentwise
    h2_ok = True
    try:
        if id_H not in H: h2_ok = False
        for h in H:
            if op_H(id_H, h) != h or op_H(h, id_H) != h: h2_ok = False
            has_inv = False
            for inv in H:
                if op_H(h, inv) == id_H and op_H(inv, h) == id_H:
                    has_inv = True
                    break
            if not has_inv: h2_ok = False
        for h1 in H:
            for h2 in H:
                if op_H(h1, h2) not in H: h2_ok = False
                for h3 in H:
                    if op_H(h1, op_H(h2, h3)) != op_H(op_H(h1, h2), h3): h2_ok = False

        def induced_a(g, x):
            res = action_GH((g, id_H), (x, y_w))
            return res[0] if isinstance(res, (tuple, list)) and len(res) > 0 else None

        def induced_b(h, y):
            res = action_GH((id_G, h), (x_w, y))
            return res[1] if isinstance(res, (tuple, list)) and len(res) > 1 else None

        for x in X:
            for y in Y:
                res_id = action_GH((id_G, id_H), (x, y))
                if not (isinstance(res_id, (tuple, list)) and len(res_id) == 2 and res_id[0] == x and res_id[1] == y):
                    h2_ok = False
                
                for g1 in G:
                    for h1 in H:
                        res1 = action_GH((g1, h1), (x, y))
                        if not (isinstance(res1, (tuple, list)) and len(res1) == 2):
                            h2_ok = False
                        else:
                            if res1[0] not in X or res1[1] not in Y:
                                h2_ok = False
                            if res1[0] != induced_a(g1, x): h2_ok = False
                            if res1[1] != induced_b(h1, y): h2_ok = False
                        
                        for g2 in G:
                            for h2 in H:
                                res2 = action_GH((g2, h2), (x, y))
                                res_comp1 = action_GH((g1, h1), res2)
                                res_comp2 = action_GH((op_G(g1, g2), op_H(h1, h2)), (x, y))
                                if not (isinstance(res_comp1, (tuple, list)) and isinstance(res_comp2, (tuple, list)) and len(res_comp1) == 2 and len(res_comp2) == 2 and res_comp1[0] == res_comp2[0] and res_comp1[1] == res_comp2[1]):
                                    h2_ok = False
    except Exception:
        h2_ok = False

    # H3: (x, y) is an element of X \times Y
    h3_ok = True
    try:
        if x_w not in X or y_w not in Y:
            h3_ok = False
    except Exception:
        h3_ok = False

    # Conclusion: The stabilizer of (x, y) in G \times H is the direct product of the stabilizer of x in G and the stabilizer of y in H
    neg_q_ok = False
    try:
        Stab_GH = []
        for g in G:
            for h in H:
                res = action_GH((g, h), (x_w, y_w))
                if isinstance(res, (tuple, list)) and len(res) == 2 and res[0] == x_w and res[1] == y_w:
                    if (g, h) not in Stab_GH:
                        Stab_GH.append((g, h))
        
        Stab_G = []
        for g in G:
            if action_G(g, x_w) == x_w:
                if g not in Stab_G:
                    Stab_G.append(g)
        
        Stab_H = []
        if 'action_H' in witness:
            action_H = witness['action_H']
            for h in H:
                if action_H(h, y_w) == y_w:
                    if h not in Stab_H:
                        Stab_H.append(h)
        else:
            for h in H:
                if induced_b(h, y_w) == y_w:
                    if h not in Stab_H:
                        Stab_H.append(h)
        
        DirectProduct = []
        for g in Stab_G:
            for h in Stab_H:
                if (g, h) not in DirectProduct:
                    DirectProduct.append((g, h))
        
        def is_equal_unordered(list1, list2):
            if len(list1) != len(list2):
                return False
            l2_copy = list(list2)
            for item in list1:
                found = False
                for i, item2 in enumerate(l2_copy):
                    if item == item2:
                        found = True
                        l2_copy.pop(i)
                        break
                if not found:
                    return False
            return True

        if not is_equal_unordered(Stab_GH, DirectProduct):
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: The direct product G \\times H acts on the Cartesian product X \\times Y componentwise",
    "H_3: (x, y) is an element of X \\times Y",
    "¬Q: The stabilizer of (x, y) in G \\times H is NOT the direct product of the stabilizer of x in G and the stabilizer of y in H"
]

N_HYP = 3
NEG_Q_INDEX = 3