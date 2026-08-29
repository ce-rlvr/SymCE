import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    p, G = None, None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p, G = witness
        else:
            G = witness
            order = int(G.order())
            p = math.isqrt(order)
            if p**2 != order:
                p = 0
    except Exception:
        pass

    try:
        h1_ok = bool(sympy.ntheory.isprime(p))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(G.order() == p**2)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not bool(G.is_abelian)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: The order of G is p^2",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2