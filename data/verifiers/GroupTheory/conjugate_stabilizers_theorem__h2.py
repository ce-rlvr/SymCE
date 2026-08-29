import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
        G, X, action, x, g, y = witness
    except Exception:
        return [False] * 5 + [False]

    def act(g_elem, x_elem):
        if isinstance(action, dict):
            return action[(g_elem, x_elem)]
        else:
            return action(g_elem, x_elem)

    # H1: G is a group
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        if hasattr(G, 'identity'):
            id_elem = G.identity
        else:
            id_elem = None
            for e in elements:
                if e * e == e:
                    id_elem = e
                    break
                    
        if isinstance(G, PermutationGroup):
            h1 = True
        else:
            h1 = id_elem is not None
            if h1:
                for a in elements:
                    has_inv = False
                    for b in elements:
                        if a * b == id_elem and b * a == id_elem:
                            has_inv = True
                            break
                    if not has_inv:
                        h1 = False
                        break
                    for b in elements:
                        if a * b not in elements:
                            h1 = False
                            break
    except Exception:
        h1 = False
        elements = []
        id_elem = None

    # H2: G acts on X
    try:
        h2 = True
        for x_elem in X:
            if act(id_elem, x_elem) != x_elem:
                h2 = False
                break
        if h2:
            is_left = True
            is_right = True
            for g1 in elements:
                for g2 in elements:
                    for x_elem in X:
                        res = act(g1 * g2, x_elem)
                        if res != act(g1, act(g2, x_elem)):
                            is_left = False
                        if res != act(g2, act(g1, x_elem)):
                            is_right = False
                    if not is_left and not is_right:
                        break
                if not is_left and not is_right:
                    break
            h2 = is_left or is_right
    except Exception:
        h2 = False

    # H3: x \in X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # H4: g \in G
    try:
        h4 = g in elements
    except Exception:
        h4 = False

    # H5: y = g \cdot x
    try:
        h5 = y == act(g, x)
    except Exception:
        h5 = False

    # neg_Q: Stab(y) != g Stab(x) g^{-1}
    try:
        g_inv = None
        if hasattr(g, '__invert__'):
            try:
                g_inv = ~g
            except Exception:
                pass
        if g_inv is None and hasattr(g, 'inv'):
            try:
                g_inv = g.inv()
            except Exception:
                pass
        if g_inv is None:
            for e in elements:
                if g * e == id_elem and e * g == id_elem:
                    g_inv = e
                    break
                    
        stab_x = []
        for h in elements:
            if act(h, x) == x:
                stab_x.append(h)
                
        stab_y = []
        for h in elements:
            if act(h, y) == y:
                stab_y.append(h)
                
        g_stab_x_g_inv = []
        for h in stab_x:
            val = g * h * g_inv
            g_stab_x_g_inv.append(val)
            
        def is_subset(list1, list2):
            for item1 in list1:
                if item1 not in list2:
                    return False
            return True
            
        sets_equal = is_subset(stab_y, g_stab_x_g_inv) and is_subset(g_stab_x_g_inv, stab_y)
        neg_q = not sets_equal
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G acts on X",
    "H_3: x in X",
    "H_4: g in G",
    "H_5: y = g \\cdot x",
    "¬Q: Stab(y) != g Stab(x) g^{-1}"
]

N_HYP = 5
NEG_Q_INDEX = 5