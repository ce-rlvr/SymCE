import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for named objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)  # V4 is often represented as a subgroup of A4, but we'll leave it as A4 for simplicity
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
    """
    Given a witness (G, x, y), checks if it is a valid counterexample to the false conjecture.
    """
    try:
        G, x, y = witness
    except Exception:
        return [False] * 6 + [False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) or hasattr(G, 'is_group')
    except Exception:
        h1 = False

    # H_2: y is an element of G
    try:
        h2 = y in G.elements if hasattr(G, 'elements') else y in G
    except Exception:
        h2 = False

    # H_3: x and y commute
    try:
        h3 = (x * y == y * x)
    except Exception:
        h3 = False

    # H_4: x has finite order
    try:
        order_x = x.order() if hasattr(x, 'order') else None
        h4 = order_x is not None and order_x > 0
    except Exception:
        h4 = False

    # H_5: y has finite order
    try:
        order_y = y.order() if hasattr(y, 'order') else None
        h5 = order_y is not None and order_y > 0
    except Exception:
        h5 = False

    # H_6: The orders of x and y are coprime
    try:
        h6 = math.gcd(order_x, order_y) == 1
    except Exception:
        h6 = False

    # ¬Q: The centralizer of xy in G is NOT equal to the intersection of the centralizer of x in G and the centralizer of y in G
    try:
        xy = x * y
        
        # Centralizer of xy in G
        C_G_xy = set()
        for g in G.elements if hasattr(G, 'elements') else G:
            if g * xy == xy * g:
                C_G_xy.add(g)
                
        # Centralizer of x in G
        C_G_x = set()
        for g in G.elements if hasattr(G, 'elements') else G:
            if g * x == x * g:
                C_G_x.add(g)
                
        # Centralizer of y in G
        C_G_y = set()
        for g in G.elements if hasattr(G, 'elements') else G:
            if g * y == y * g:
                C_G_y.add(g)
                
        intersection = C_G_x.intersection(C_G_y)
        
        neg_q = (C_G_xy != intersection)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: y is an element of G",
    "H_3: x and y commute",
    "H_4: x has finite order",
    "H_5: y has finite order",
    "H_6: The orders of x and y are coprime",
    "¬Q: The centralizer of xy in G is not equal to the intersection of the centralizer of x in G and the centralizer of y in G"
]

N_HYP = 6
NEG_Q_INDEX = 6