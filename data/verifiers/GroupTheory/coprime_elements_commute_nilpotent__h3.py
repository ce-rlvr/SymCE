import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = False
        if isinstance(G, PermutationGroup):
            h1 = True
        elif hasattr(G, 'is_group') and G.is_group:
            o = G.order() if callable(G.order) else G.order
            if o > 0 and o < float('inf'):
                h1 = True
    except Exception:
        h1 = False

    # H_2: G is a nilpotent group
    try:
        if callable(G.is_nilpotent):
            h2 = bool(G.is_nilpotent())
        else:
            h2 = bool(G.is_nilpotent)
    except Exception:
        h2 = False

    # H_3: The order of x and the order of y are relatively prime integers
    try:
        ox = x.order() if callable(x.order) else x.order
        oy = y.order() if callable(y.order) else y.order
        h3 = math.gcd(int(ox), int(oy)) == 1
    except Exception:
        h3 = False

    # ¬Q: x and y do not commute
    try:
        neg_q = (x * y) != (y * x)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a nilpotent group",
    "H_3: The order of x and the order of y are relatively prime integers",
    "¬Q: x and y do not commute"
]

N_HYP = 3
NEG_Q_INDEX = 3