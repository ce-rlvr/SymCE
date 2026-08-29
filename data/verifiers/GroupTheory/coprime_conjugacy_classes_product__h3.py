import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        G, x, y = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() <= 2000
    except Exception:
        h1 = False

    try:
        h2 = x in G and y in G
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            C_x = set(g for g in G.elements if g * x == x * g)
            C_y = set(g for g in G.elements if g * y == y * g)
            C_xy = C_x.intersection(C_y)
            size_prod = len(C_x) * len(C_y) // len(C_xy)
            neg_q = size_prod != G.order()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x and y are elements of G",
    "¬Q: G does not factorize as the product of their centralizers (G != C_G(x) C_G(y))"
]

N_HYP = 2
NEG_Q_INDEX = 2