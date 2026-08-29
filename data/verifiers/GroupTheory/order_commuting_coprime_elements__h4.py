import math
import sympy
from sympy.combinatorics import PermutationGroup
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
        if len(witness) != 3:
            return [False] * 7
        G, g, h = witness
    except Exception:
        return [False] * 7

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = g in G
    except Exception:
        h2 = False

    try:
        h3 = h in G
    except Exception:
        h3 = False

    try:
        m = g.order()
        h4 = int(m) == m and m > 0
    except Exception:
        h4 = False

    try:
        n = h.order()
        h5 = int(n) == n and n > 0
    except Exception:
        h5 = False

    try:
        h6 = math.gcd(int(m), int(n)) == 1
    except Exception:
        h6 = False

    try:
        gh = g * h
        neg_q = gh.order() != m * n
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: G is a group",
    "H_2: g is an element of G",
    "H_3: h is an element of G",
    "H_4: the order of g is a finite integer m",
    "H_5: the order of h is a finite integer n",
    "H_6: gcd(m, n) = 1",
    "¬Q: The order of the product gh is not exactly m * n"
]

N_HYP: int = 6
NEG_Q_INDEX: int = 6