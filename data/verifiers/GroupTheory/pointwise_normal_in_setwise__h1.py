import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.matrices import eye, zeros, Matrix

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

def get_elements(obj):
    if hasattr(obj, 'elements'):
        try:
            return set(obj.elements)
        except Exception:
            pass
    if hasattr(obj, 'generate') and callable(obj.generate):
        try:
            return set(obj.generate())
        except Exception:
            pass
    return set(obj)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 5:
                G, X, Y, G_Y, G_pY = witness
            elif len(witness) == 3:
                G, X, Y = witness
                G_Y = None
                G_pY = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: Y is a subset of X
    try:
        X_set = set(X)
        Y_set = set(Y)
        h1 = Y_set.issubset(X_set)
    except Exception:
        h1 = False

    def apply_action(g, y):
        try:
            return g(y)
        except Exception:
            return g * y

    def get_inv(g):
        try:
            return g**-1
        except Exception:
            return ~g

    # H2: G_Y is the setwise stabilizer of Y in G
    try:
        G_elems = get_elements(G)
        actual_G_Y = set()
        for g in G_elems:
            try:
                img = {apply_action(g, y) for y in Y_set}
                if img == Y_set:
                    actual_G_Y.add(g)
            except Exception:
                pass
        
        if G_Y is not None:
            h2 = (get_elements(G_Y) == actual_G_Y)
        else:
            G_Y = actual_G_Y
            h2 = True
    except Exception:
        h2 = False

    # H3: G_{(Y)} is the pointwise stabilizer of Y in G
    try:
        G_elems = get_elements(G)
        actual_G_pY = set()
        for g in G_elems:
            try:
                if all(apply_action(g, y) == y for y in Y_set):
                    actual_G_pY.add(g)
            except Exception:
                pass
        
        if G_pY is not None:
            h3 = (get_elements(G_pY) == actual_G_pY)
        else:
            G_pY = actual_G_pY
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: G_{(Y)} is NOT a normal subgroup of G_Y
    try:
        G_Y_elems = get_elements(G_Y)
        G_pY_elems = get_elements(G_pY)
        
        def is_group(elems):
            if not elems:
                return False
            for g in elems:
                try:
                    inv = get_inv(g)
                except Exception:
                    return False
                if inv not in elems:
                    return False
                for h in elems:
                    try:
                        prod = g * h
                    except Exception:
                        return False
                    if prod not in elems:
                        return False
            return True

        if not is_group(G_Y_elems):
            neg_q = True
        elif not is_group(G_pY_elems):
            neg_q = True
        else:
            if not G_pY_elems.issubset(G_Y_elems):
                neg_q = True
            else:
                is_normal = True
                for h in G_pY_elems:
                    for g in G_Y_elems:
                        try:
                            conj = g * h * get_inv(g)
                        except Exception:
                            is_normal = False
                            break
                        if conj not in G_pY_elems:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Y is a subset of X",
    "H_2: G_Y is the setwise stabilizer of Y in G",
    "H_3: G_{(Y)} is the pointwise stabilizer of Y in G",
    "¬Q: G_{(Y)} is not a normal subgroup of G_Y"
]

N_HYP = 3
NEG_Q_INDEX = 3