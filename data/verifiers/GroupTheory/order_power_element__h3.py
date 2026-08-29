import math
from sympy.combinatorics import PermutationGroup, Permutation
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

def conditions(witness):
    try:
        if len(witness) == 4:
            G, g, k, n = witness
        elif len(witness) == 3:
            G, g, k = witness
            try:
                n = G.order()
            except Exception:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H2: g is an element of G
    try:
        h2_ok = g in G
    except Exception:
        h2_ok = False

    # H3: k is an integer
    try:
        h3_ok = isinstance(k, int)
    except Exception:
        h3_ok = False

    # neg_Q: The order of the element g^k is NOT n / gcd(n, k)
    try:
        if not isinstance(n, int):
            neg_q_ok = False
        else:
            g_k = g ** k
            actual_order = g_k.order()
            expected_order = n / math.gcd(n, k)
            neg_q_ok = actual_order != expected_order
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g is an element of G",
    "H_3: k is an integer",
    "¬Q: The order of the element g^k is not n / gcd(n, k)"
]

N_HYP = 3
NEG_Q_INDEX = 3