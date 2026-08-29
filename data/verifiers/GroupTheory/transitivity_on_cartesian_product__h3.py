import itertools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness):
    try:
        G = witness['G']
        if hasattr(G, 'elements'):
            G_elems = list(G.elements)
            op = lambda a, b: a * b
        else:
            G_elems = list(G)
            op = witness.get('op', lambda a, b: a * b)
            
        X = list(witness['X'])
        Y = list(witness['Y'])
        
        action_X_raw = witness['action_X']
        if callable(action_X_raw):
            action_X = action_X_raw
        else:
            action_X = lambda g, x: action_X_raw[g][x]
            
        action_Y_raw = witness['action_Y']
        if callable(action_Y_raw):
            action_Y = action_Y_raw
        else:
            action_Y = lambda g, y: action_Y_raw[g][y]
            
        x_elem = witness['x']
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = False
        if G_elems:
            closure_ok = True
            for g1 in G_elems:
                for g2 in G_elems:
                    try:
                        if op(g1, g2) not in G_elems:
                            closure_ok = False
                            break
                    except Exception:
                        closure_ok = False
                        break
                if not closure_ok: break
            
            if closure_ok:
                id_elem = None
                for e in G_elems:
                    try:
                        if all(op(e, g) == g and op(g, e) == g for g in G_elems):
                            id_elem = e
                            break
                    except Exception:
                        pass
                
                if id_elem is not None:
                    inv_ok = True
                    for g in G_elems:
                        try:
                            if not any(op(g, h) == id_elem and op(h, g) == id_elem for h in G_elems):
                                inv_ok = False
                                break
                        except Exception:
                            inv_ok = False
                            break
                    
                    if inv_ok:
                        assoc_ok = True
                        if not all(isinstance(g, Permutation) for g in G_elems):
                            for g1 in G_elems:
                                for g2 in G_elems:
                                    for g3 in G_elems:
                                        try:
                                            if op(g1, op(g2, g3)) != op(op(g1, g2), g3):
                                                assoc_ok = False
                                                break
                                        except Exception:
                                            assoc_ok = False
                                            break
                                    if not assoc_ok: break
                                if not assoc_ok: break
                        h1 = assoc_ok
    except Exception:
        h1 = False

    def check_action(G_sub, S, action):
        if not S: return True
        id_e = None
        for e in G_sub:
            try:
                if all(op(e, g) == g and op(g, e) == g for g in G_sub):
                    id_e = e
                    break
            except Exception:
                pass
        if id_e is None: return False
        
        for s in S:
            try:
                if action(id_e, s) != s: return False
            except Exception:
                return False
                
        for g1 in G_sub:
            for g2 in G_sub:
                for s in S:
                    try:
                        if action(g1, action(g2, s)) != action(op(g1, g2), s): return False
                    except Exception:
                        return False
        return True

    # H2: G acts transitively on X
    try:
        h2 = False
        if check_action(G_elems, X, action_X):
            if X:
                x0 = X[0]
                orbit = set()
                for g in G_elems:
                    res = action_X(g, x0)
                    if isinstance(res, list): res = tuple(res)
                    orbit.add(res)
                if len(orbit) == len(X):
                    h2 = True
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = x_elem in X
    except Exception:
        h3 = False

    # Conclusion: The diagonal action of G on X \times Y is transitive iff G_x acts transitively on Y
    try:
        neg_q = False
        if check_action(G_elems, Y, action_Y):
            # Diagonal action of G on X x Y is transitive?
            diag_transitive = False
            if X and Y:
                xy0 = (X[0], Y[0])
                orbit_diag = set()
                for g in G_elems:
                    rx = action_X(g, xy0[0])
                    ry = action_Y(g, xy0[1])
                    if isinstance(rx, list): rx = tuple(rx)
                    if isinstance(ry, list): ry = tuple(ry)
                    orbit_diag.add((rx, ry))
                if len(orbit_diag) == len(X) * len(Y):
                    diag_transitive = True
            elif not X and not Y:
                diag_transitive = True
                
            # G_x acts transitively on Y?
            G_x = []
            for g in G_elems:
                if action_X(g, x_elem) == x_elem:
                    G_x.append(g)
                    
            Gx_transitive = False
            if Y:
                y0 = Y[0]
                orbit_y = set()
                for g in G_x:
                    ry = action_Y(g, y0)
                    if isinstance(ry, list): ry = tuple(ry)
                    orbit_y.add(ry)
                if len(orbit_y) == len(Y):
                    Gx_transitive = True
            elif not Y:
                Gx_transitive = True
                
            # The conclusion is: diag_transitive == Gx_transitive
            # Negation of conclusion: diag_transitive != Gx_transitive
            neg_q = (diag_transitive != Gx_transitive)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts transitively on X",
    "H_3: x is an element of X",
    "¬Q: The diagonal action of G on X \\times Y is transitive if and only if the stabilizer G_x acts transitively on Y is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3