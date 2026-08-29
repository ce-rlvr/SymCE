import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup
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
        G, H, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: The index of N in G is finite
    try:
        h3 = isinstance(N, PermutationGroup) and N.is_subgroup(G)
    except Exception:
        h3 = False

    # ¬Q: The index of H cap N in H is finite and <= index of N in G FAILS
    try:
        h_elems = set(H.generate())
        n_elems = set(N.generate())
        order_int = len(h_elems.intersection(n_elems))
        
        h_order = H.order() if callable(getattr(H, 'order', None)) else H.order
        n_order = N.order() if callable(getattr(N, 'order', None)) else N.order
        g_order = G.order() if callable(getattr(G, 'order', None)) else G.order
        
        index_H_int_N = h_order // order_int
        index_G_N = g_order // n_order
        
        neg_q = bool(index_H_int_N > index_G_N)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: The index of N in G is finite",
    "¬Q: index of H cap N in H is greater than index of N in G"
]

N_HYP = 3
NEG_Q_INDEX = 3