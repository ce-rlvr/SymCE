import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 5:
            return [False] * 7
        G, g, h, m, n = witness
    except Exception:
        return [False] * 7

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: g is an element of G
    try:
        h2 = g in G
    except Exception:
        h2 = False

    # H_3: h is an element of G
    try:
        h3 = h in G
    except Exception:
        h3 = False

    # H_4: g and h commute (gh = hg)
    try:
        h4 = bool(g * h == h * g)
    except Exception:
        h4 = False

    # H_5: the order of g is a finite integer m
    try:
        h5 = bool(g.order() == m)
    except Exception:
        h5 = False

    # H_6: gcd(m, n) = 1
    try:
        h6 = bool(math.gcd(int(m), int(n)) == 1)
    except Exception:
        h6 = False

    # ¬Q: The order of the product gh is not exactly m * n
    try:
        neg_q = bool((g * h).order() != m * n)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G",
    "H_3: h is an element of G",
    "H_4: g and h commute (gh = hg)",
    "H_5: the order of g is a finite integer m",
    "H_6: gcd(m, n) = 1",
    "¬Q: The order of the product gh is not exactly m * n"
]

N_HYP = 6
NEG_Q_INDEX = 6