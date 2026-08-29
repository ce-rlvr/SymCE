import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
        if len(witness) != 3:
            return [False] * 7
        G, x, y = witness
    except Exception:
        return [False] * 7

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: x is an element of G
    try:
        h2 = h1 and (x in G)
    except Exception:
        h2 = False

    # H_3: y is an element of G
    try:
        h3 = h1 and (y in G)
    except Exception:
        h3 = False

    # H_4: x has finite order
    try:
        h4 = h2 and x.order() > 0
    except Exception:
        h4 = False

    # H_5: y has finite order
    try:
        h5 = h3 and y.order() > 0
    except Exception:
        h5 = False

    # H_6: The orders of x and y are coprime
    try:
        h6 = h4 and h5 and math.gcd(x.order(), y.order()) == 1
    except Exception:
        h6 = False

    # ¬Q: The centralizer of xy in G is not equal to the intersection of the centralizer of x in G and the centralizer of y in G
    try:
        neg_q = False
        if h1 and h2 and h3:
            xy = x * y
            elements = []
            too_large = False
            # Limit the size to prevent hanging on unreasonably large witness groups
            for i, g in enumerate(G.generate()):
                if i > 5000:
                    too_large = True
                    break
                elements.append(g)
            
            if not too_large:
                C_xy = set(g for g in elements if g * xy == xy * g)
                C_x = set(g for g in elements if g * x == x * g)
                C_y = set(g for g in elements if g * y == y * g)
                intersection = C_x.intersection(C_y)
                neg_q = C_xy != intersection
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "H_3: y is an element of G",
    "H_4: x has finite order",
    "H_5: y has finite order",
    "H_6: The orders of x and y are coprime",
    "¬Q: The centralizer of xy in G is not equal to the intersection of the centralizer of x in G and the centralizer of y in G"
]

N_HYP = 6
NEG_Q_INDEX = 6