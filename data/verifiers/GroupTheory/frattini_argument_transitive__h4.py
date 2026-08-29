import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    "H_1: G is a group acting on a set X",
    "H_2: N is a normal subgroup of G",
    "H_3: N acts transitively on X",
    "¬Q: G != N G_x (where G_x is the stabilizer of x in G)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def contains(G, g):
    if hasattr(G, 'contains'):
        return G.contains(g)
    return g in G

def is_normal_subgroup(N, G):
    for n in N.generators:
        if not contains(G, n):
            return False
    for g in G.generators:
        g_inv = ~g
        for n in N.generators:
            conj = g * n * g_inv
            if not contains(N, conj):
                return False
    return True

def get_stabilizer(G, x):
    if not isinstance(x, int):
        raise ValueError("x must be an integer")
    if hasattr(G, 'degree') and x >= G.degree:
        return G
    return G.stabilizer(x)

def get_orbit(G, x):
    if not isinstance(x, int):
        raise ValueError("x must be an integer")
    if hasattr(G, 'degree') and x >= G.degree:
        return {x}
    return set(G.orbit(x))

def get_order(G):
    order = G.order
    if callable(order):
        return order()
    return order

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            N = witness.get('N')
            x = witness.get('x')
        else:
            G, X, N, x = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group acting on a set X
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            X_set = set(X)
            h1 = True
            for g in G.generators:
                for i in X_set:
                    if g(i) not in X_set:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = is_normal_subgroup(N, G)
    except Exception:
        h2 = False

    # H3: N acts transitively on X
    try:
        if not X_set:
            h3 = True
        else:
            x0 = list(X_set)[0]
            orb = get_orbit(N, x0)
            h3 = (orb == X_set)
    except Exception:
        h3 = False

    # ¬Q: G != N G_x
    try:
        Gx = get_stabilizer(G, x)
        
        if hasattr(N, 'intersection'):
            inter = N.intersection(Gx)
            inter_order = get_order(inter)
        elif hasattr(N, 'intersect'):
            inter = N.intersect(Gx)
            inter_order = get_order(inter)
        else:
            inter_elems = set(N.generate()).intersection(set(Gx.generate()))
            inter_order = len(inter_elems)
            
        size_NGx = (get_order(N) * get_order(Gx)) // inter_order
        neg_q = size_NGx != get_order(G)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]