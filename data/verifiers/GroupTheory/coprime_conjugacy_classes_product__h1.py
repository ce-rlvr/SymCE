import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False]

    # H1: x and y are elements of G
    try:
        order = G.order() if callable(G.order) else G.order
        if order > 5000:
            h1 = False
        else:
            h1 = bool(G.contains(x) and G.contains(y))
    except Exception:
        h1 = False

    # H2: The size of the conjugacy class of x and the size of the conjugacy class of y are relatively prime
    try:
        if not h1:
            h2 = False
        else:
            elements = list(G.elements)
            n_elements = len(elements)
            
            Cx = [g for g in elements if g * x == x * g]
            Cy = [g for g in elements if g * y == y * g]
            
            cl_x = int(n_elements // len(Cx))
            cl_y = int(n_elements // len(Cy))
            
            h2 = bool(math.gcd(cl_x, cl_y) == 1)
    except Exception:
        h2 = False

    # neg_Q: G does not factorize as the product of their centralizers (G != C_G(x) C_G(y))
    try:
        if not h1:
            neg_q = False
        else:
            elements = list(G.elements)
            n_elements = len(elements)
            
            Cx = [g for g in elements if g * x == x * g]
            Cy = [g for g in elements if g * y == y * g]
            
            Cx_set = set(Cx)
            intersection_size = sum(1 for g in Cy if g in Cx_set)
            
            # Size of the product set C_G(x) C_G(y)
            prod_size = (len(Cx) * len(Cy)) // intersection_size
            
            neg_q = bool(prod_size != n_elements)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "H_2: The size of the conjugacy class of x and the size of the conjugacy class of y are relatively prime",
    "¬Q: G does not factorize as the product of their centralizers (G != C_G(x) C_G(y))"
]

N_HYP = 2
NEG_Q_INDEX = 2