import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            g = witness.get('g')
            h = witness.get('h')
            m = witness.get('m')
            n = witness.get('n')
        else:
            G, g, h, m, n = witness
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
        h4 = (g * h == h * g)
    except Exception:
        h4 = False

    try:
        h5 = (h.order() == n) and (int(n) == n)
    except Exception:
        h5 = False

    try:
        h6 = (int(m) == m) and (int(n) == n) and (math.gcd(int(m), int(n)) == 1)
    except Exception:
        h6 = False

    try:
        gh = g * h
        neg_q = (gh.order() != m * n)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, h6, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G",
    "H_3: h is an element of G",
    "H_4: g and h commute (gh = hg)",
    "H_5: the order of h is a finite integer n",
    "H_6: gcd(m, n) = 1",
    "¬Q: The order of the product gh is not exactly m * n"
]

N_HYP = 6
NEG_Q_INDEX = 6