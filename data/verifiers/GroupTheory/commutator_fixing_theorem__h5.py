import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness) -> list[bool]:
    try:
        G, g, h, x = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: g and h are elements of G
    try:
        h2 = g in G and h in G
    except Exception:
        h2 = False

    # H_3: x is an element of X
    try:
        h3 = isinstance(x, int) and 0 <= x < G.degree
    except Exception:
        h3 = False

    # H_4: x is fixed by g
    try:
        h4 = g(x) == x
    except Exception:
        h4 = False

    # ¬Q: The element x is NOT fixed by the commutator
    try:
        comm = (g**-1) * (h**-1) * g * h
        neg_q = comm(x) != x
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: g and h are elements of G",
    "H_3: x is an element of X",
    "H_4: x is fixed by g",
    "¬Q: x is not fixed by the commutator of g and h"
]

N_HYP = 4
NEG_Q_INDEX = 4