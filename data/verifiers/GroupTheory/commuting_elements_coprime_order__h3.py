import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from math import gcd

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
        G, a, b = witness
    except Exception:
        return [False] * 6

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup) or hasattr(G, 'identity')
    except Exception:
        h1 = False

    # H_2: a and b are elements of G
    try:
        h2 = (a in G) and (b in G)
    except Exception:
        h2 = False

    # H_3: The order of a is a finite integer m
    try:
        m = a.order()
        h3 = (int(m) > 0)
    except Exception:
        h3 = False

    # H_4: The order of b is a finite integer n
    try:
        n = b.order()
        h4 = (int(n) > 0)
    except Exception:
        h4 = False

    # H_5: \gcd(m, n) = 1
    try:
        h5 = gcd(int(m), int(n)) == 1
    except Exception:
        h5 = False

    # ¬Q: The order of the product ab is not mn
    try:
        ab = a * b
        neg_q = ab.order() != m * n
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: a and b are elements of G",
    "H_3: The order of a is a finite integer m",
    "H_4: The order of b is a finite integer n",
    "H_5: gcd(m, n) = 1",
    "¬Q: The order of the product ab is not mn"
]

N_HYP = 5
NEG_Q_INDEX = 5