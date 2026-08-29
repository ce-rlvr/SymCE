import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
        G, x, y = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: x and y are conjugate in G
    try:
        h2 = False
        if h1:
            for g in G.generate():
                if g * x * ~g == y:
                    h2 = True
                    break
    except Exception:
        h2 = False

    # ¬Q: The order of x is not equal to the order of y
    try:
        if hasattr(x, 'order') and hasattr(y, 'order'):
            ox = x.order() if callable(x.order) else x.order
            oy = y.order() if callable(y.order) else y.order
            neg_q = (ox != oy)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are conjugate in G",
    "¬Q: The order of x is not equal to the order of y"
]

N_HYP = 2
NEG_Q_INDEX = 2