import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
        G, x = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: x is a non-identity element of G
    try:
        in_G = (x in G)
        not_id = not x.is_Identity
        h2 = bool(in_G and not_id)
    except Exception:
        h2 = False

    # ¬Q: x is conjugate to x^-1 in G
    try:
        x_inv = ~x
        neg_q = False
        for g in G.elements:
            if g * x * ~g == x_inv:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is a non-identity element of G",
    "¬Q: x is conjugate to x^-1 in G"
]

N_HYP = 2
NEG_Q_INDEX = 2