import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    "H_1: G is a group acting on a set X",
    "H_2: H is a group acting on a set Y",
    "H_3: (x, y) is an element of X \\times Y",
    "¬Q: The stabilizer of (x, y) in G \\times H is not the direct product of the stabilizer of x in G and the stabilizer of y in H"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    def get_elements(group_obj):
        if hasattr(group_obj, 'elements'):
            return list(group_obj.elements)
        elif hasattr(group_obj, 'generate'):
            return list(group_obj.generate())
        else:
            return list(group_obj)

    try:
        G = get_elements(witness['G'])
        H = get_elements(witness['H'])
        X = list(witness['X'])
        Y = list(witness['Y'])
        action_G = witness['action_G']
        action_H = witness['action_H']
        action_GH = witness['action_GH']
        x = witness['x']
        y = witness['y']
    except Exception:
        return [False, False, False, False]

    def find_identity(elements):
        for e in elements:
            try:
                if all(e * g == g and g * e == g for g in elements):
                    return e
            except Exception:
                continue
        return None

    def is_group(elements):
        if not elements: return False
        id_e = find_identity(elements)
        if id_e is None: return False
        for g in elements:
            if not any(g * inv == id_e and inv * g == id_e for inv in elements):
                return False
            for h in elements:
                if g * h not in elements:
                    return False
        for a in elements:
            for b in elements:
                for c in elements:
                    if (a * b) * c != a * (b * c):
                        return False
        return True

    def is_valid_action(G_elems, X_elems, action):
        id_G = find_identity(G_elems)
        if id_G is None: return False
        for x_elem in X_elems:
            if action(id_G, x_elem) != x_elem:
                return False
        
        is_left = True
        is_right = True
        for g1 in G_elems:
            for g2 in G_elems:
                for x_elem in X_elems:
                    val_prod = action(g1 * g2, x_elem)
                    if val_prod != action(g1, action(g2, x_elem)):
                        is_left = False
                    if val_prod != action(g2, action(g1, x_elem)):
                        is_right = False
                    if not is_left and not is_right:
                        return False
        return True

    # H1: G is a group acting on a set X.
    try:
        h1 = is_group(G) and is_valid_action(G, X, action_G)
    except Exception:
        h1 = False

    # H2: H is a group acting on a set Y.
    try:
        h2 = is_group(H) and is_valid_action(H, Y, action_H)
    except Exception:
        h2 = False

    # H3: (x, y) is an element of X \times Y.
    try:
        h3 = (x in X) and (y in Y)
    except Exception:
        h3 = False

    # Conclusion: The stabilizer of (x, y) in G \times H is the direct product of the stabilizer of x in G and the stabilizer of y in H.
    try:
        id_G = find_identity(G)
        id_H = find_identity(H)
        if id_G is None or id_H is None:
            valid_GH = False
        else:
            valid_GH = True
            for x_elem in X:
                for y_elem in Y:
                    if action_GH(id_G, id_H, x_elem, y_elem) != (x_elem, y_elem):
                        valid_GH = False
                        break
                if not valid_GH: break
            
            if valid_GH:
                is_left_GH = True
                is_right_GH = True
                for g1 in G:
                    for h1 in H:
                        for g2 in G:
                            for h2 in H:
                                for x_elem in X:
                                    for y_elem in Y:
                                        val_prod = action_GH(g1 * g2, h1 * h2, x_elem, y_elem)
                                        
                                        res_g2_h2 = action_GH(g2, h2, x_elem, y_elem)
                                        if val_prod != action_GH(g1, h1, res_g2_h2[0], res_g2_h2[1]):
                                            is_left_GH = False
                                            
                                        res_g1_h1 = action_GH(g1, h1, x_elem, y_elem)
                                        if val_prod != action_GH(g2, h2, res_g1_h1[0], res_g1_h1[1]):
                                            is_right_GH = False
                                            
                                        if not is_left_GH and not is_right_GH:
                                            break
                                    if not is_left_GH and not is_right_GH: break
                                if not is_left_GH and not is_right_GH: break
                            if not is_left_GH and not is_right_GH: break
                        if not is_left_GH and not is_right_GH: break
                    if not is_left_GH and not is_right_GH: break
                valid_GH = is_left_GH or is_right_GH

        if not valid_GH:
            neg_q = False
        else:
            stab_GH = []
            for g in G:
                for h in H:
                    if action_GH(g, h, x, y) == (x, y):
                        if (g, h) not in stab_GH:
                            stab_GH.append((g, h))
            
            stab_G = []
            for g in G:
                if action_G(g, x) == x:
                    if g not in stab_G:
                        stab_G.append(g)
            
            stab_H = []
            for h in H:
                if action_H(h, y) == y:
                    if h not in stab_H:
                        stab_H.append(h)
            
            stab_G_times_H = []
            for g in stab_G:
                for h in stab_H:
                    if (g, h) not in stab_G_times_H:
                        stab_G_times_H.append((g, h))
            
            is_subset1 = all(elem in stab_G_times_H for elem in stab_GH)
            is_subset2 = all(elem in stab_GH for elem in stab_G_times_H)
            neg_q = not (is_subset1 and is_subset2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]