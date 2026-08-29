import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    try:
        G, x, y, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: x and y are conjugate in G
    try:
        h2 = False
        if h1:
            if x in G and y in G:
                for g in G.elements:
                    if g * x * ~g == y:
                        h2 = True
                        break
    except Exception:
        h2 = False

    # H_3: n is an integer
    try:
        h3 = isinstance(n, int) and not isinstance(n, bool)
    except Exception:
        h3 = False

    # neg_Q: x^n and y^n are NOT conjugate in G
    try:
        neg_q = False
        if h1 and h3:
            xn = x**n
            yn = y**n
            if xn in G and yn in G:
                are_conjugate = False
                for g in G.elements:
                    if g * xn * ~g == yn:
                        are_conjugate = True
                        break
                neg_q = not are_conjugate
            else:
                # If they are not in G, they cannot be conjugate in G
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are conjugate in G",
    "H_3: n is an integer",
    "¬Q: x^n and y^n are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3