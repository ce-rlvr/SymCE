import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G = witness['G']
        X = witness['X']
        action = witness['action']
        g = witness['g']
        x = witness['x']
        y = witness['y']
    except Exception:
        return [False] * 6

    # H1: G is a group
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
        id_elem = G.identity
        h1 = True
    except Exception:
        h1 = False

    # H2: X is a set
    try:
        h2 = isinstance(X, (set, list, tuple))
        X_list = list(X)
    except Exception:
        h2 = False

    # H3: G acts on X
    try:
        is_left = True
        is_right = True
        for elem in X_list:
            if action(id_elem, elem) != elem:
                is_left = False
                is_right = False
                break
            for g1 in elements:
                if action(g1, elem) not in X_list:
                    is_left = False
                    is_right = False
                    break
                for g2 in elements:
                    if action(g1 * g2, elem) != action(g1, action(g2, elem)):
                        is_left = False
                    if action(g1 * g2, elem) != action(g2, action(g1, elem)):
                        is_right = False
        h3 = is_left or is_right
    except Exception:
        h3 = False

    # H4: g \in G
    try:
        h4 = g in elements
    except Exception:
        h4 = False

    # H5: y = g \cdot x
    try:
        h5 = (y == action(g, x))
    except Exception:
        h5 = False

    # neg_Q: Stab(y) != g Stab(x) g^{-1}
    try:
        stab_x = set(h for h in elements if action(h, x) == x)
        stab_y = set(h for h in elements if action(h, y) == y)
        g_inv = g**(-1)
        g_stab_x_g_inv = set(g * h * g_inv for h in stab_x)
        neg_q = (stab_y != g_stab_x_g_inv)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: X is a set",
    "H_3: G acts on X",
    "H_4: g in G",
    "H_5: y = g * x",
    "¬Q: Stab(y) != g Stab(x) g^{-1}"
]

N_HYP = 5
NEG_Q_INDEX = 5