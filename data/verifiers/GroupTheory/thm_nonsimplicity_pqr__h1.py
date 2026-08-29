import math
import itertools
import functools
import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
from sympy.abc import x, y, z
import z3

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

def conditions(witness) -> list[bool]:
    try:
        order = witness.order()
        factors = sympy.ntheory.factorint(order)
        h1 = (len(factors) == 3)
    except Exception:
        h1 = False

    try:
        order = witness.order()
        factors = sympy.ntheory.factorint(order)
        h2 = (sum(factors.values()) == 3)
    except Exception:
        h2 = False

    try:
        if hasattr(witness, 'is_simple'):
            val = witness.is_simple
            neg_q = bool(val() if callable(val) else val)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p, q, and r are distinct prime numbers",
    "H_2: The order of G is exactly p*q*r",
    "¬Q: G is a simple group"
]

N_HYP = 2
NEG_Q_INDEX = 2