import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = list(witness.get('G', []))
            X = list(witness.get('X', []))
            x = witness.get('x', None)
            y = witness.get('y', None)
            G_xy = witness.get('G_xy', None)
            if G_xy is not None: G_xy = list(G_xy)
            G_x = witness.get('G_x', None)
            if G_x is not None: G_x = list(G_x)
            G_y = witness.get('G_y', None)
            if G_y is not None: G_y = list(G_y)
        else:
            G = list(witness[0])
            X = list(witness[1])
            x = witness[2]
            y = witness[3]
            G_xy = list(witness[4]) if len(witness) > 4 else None
            G_x = list(witness[5]) if len(witness) > 5 else None
            G_y = list(witness[6]) if len(witness) > 6 else None
    except Exception:
        return [False, False, False, False]

    def act(g, pt):
        if isinstance(g, dict):
            return g.get(pt, pt)
        try:
            return g(pt)
        except TypeError:
            return g * pt

    def unique_elements(L):
        res = []
        for item in L:
            if item not in res:
                res.append(item)
        return res

    def unique_intersection(L1, L2):
        res = []
        for item in L1:
            if item in L2 and item not in res:
                res.append(item)
        return res

    def lists_equal_as_sets(L1, L2):
        for item in L1:
            if item not in L2:
                return False
        for item in L2:
            if item not in L1:
                return False
        return True

    # H1: x and y are distinct elements of X
    try:
        h1 = (x in X) and (y in X) and (x != y)
    except Exception:
        h1 = False

    # Compute stabilizers
    try:
        comp_G_xy = []
        for g in G:
            gx = act(g, x)
            gy = act(g, y)
            if lists_equal_as_sets([gx, gy], [x, y]):
                comp_G_xy.append(g)
        
        comp_G_x = []
        for g in G:
            if act(g, x) == x:
                comp_G_x.append(g)
                
        comp_G_y = []
        for g in G:
            if act(g, y) == y:
                comp_G_y.append(g)
    except Exception:
        comp_G_xy = []
        comp_G_x = []
        comp_G_y = []

    # H2: G_{x,y} is the setwise stabilizer
    try:
        if G_xy is not None:
            h2 = lists_equal_as_sets(G_xy, comp_G_xy)
            B = unique_elements(G_xy)
        else:
            h2 = True
            B = unique_elements(comp_G_xy)
    except Exception:
        h2 = False

    # H3: G_x and G_y are pointwise stabilizers
    try:
        if G_x is not None and G_y is not None:
            h3 = lists_equal_as_sets(G_x, comp_G_x) and lists_equal_as_sets(G_y, comp_G_y)
            A = unique_intersection(G_x, G_y)
        else:
            h3 = True
            A = unique_intersection(comp_G_x, comp_G_y)
    except Exception:
        h3 = False

    # Conclusion: G_x \cap G_y is a normal subgroup of G_{x,y}, and index divides 2
    try:
        def is_group(S):
            if not S:
                return False
            S_list = unique_elements(S)
            for a in S_list:
                try:
                    inv_a = a**-1
                except Exception:
                    return False
                if inv_a not in S_list:
                    return False
                for b in S_list:
                    try:
                        prod = a * b
                    except Exception:
                        return False
                    if prod not in S_list:
                        return False
            return True

        def is_normal_subgroup(sub, parent):
            if not is_group(parent):
                return False
            if not is_group(sub):
                return False
            sub_list = unique_elements(sub)
            parent_list = unique_elements(parent)
            for a in sub_list:
                if a not in parent_list:
                    return False
            for a in sub_list:
                for b in parent_list:
                    try:
                        conj = b * a * (b**-1)
                    except Exception:
                        return False
                    if conj not in sub_list:
                        return False
            return True

        is_normal = is_normal_subgroup(A, B)
        
        if is_normal and len(A) > 0 and len(B) % len(A) == 0:
            idx = len(B) // len(A)
            divides_2 = (idx in (1, 2))
        else:
            divides_2 = False
            
        q = is_normal and divides_2
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x and y are distinct elements of X",
    "H_2: G_{x,y} is the setwise stabilizer of {x, y}",
    "H_3: G_x and G_y are the pointwise stabilizers of x and y",
    "¬Q: G_x \\cap G_y is not a normal subgroup of G_{x,y} or its index does not divide 2"
]

N_HYP = 3
NEG_Q_INDEX = 3