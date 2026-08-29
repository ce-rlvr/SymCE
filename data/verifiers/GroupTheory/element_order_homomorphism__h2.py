import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        G, H, f, x = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: x is an element of G having finite order
    try:
        h2 = False
        if G.contains(x):
            order_x = x.order()
            if isinstance(order_x, (int, sympy.Integer)) and order_x > 0:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: The order of f(x) in H does not divide the order of x in G
    try:
        neg_q = False
        if isinstance(f, dict):
            fx = f[x]
        else:
            fx = f(x)
            
        if H.contains(fx):
            order_x = x.order()
            order_fx = fx.order()
            if order_x % order_fx != 0:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: x is an element of G having finite order",
    "¬Q: The order of f(x) in H does not divide the order of x in G"
]

N_HYP = 2
NEG_Q_INDEX = 2