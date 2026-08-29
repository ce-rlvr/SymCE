import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import FiniteSet
import math

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

def conditions(witness) -> list[bool]:
    try:
        G, X, k = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: X is a finite set of size n
    try:
        if isinstance(X, (set, list, tuple, range, FiniteSet)):
            n = len(X)
            h2_ok = True
        elif isinstance(X, int) and X >= 0:
            n = X
            h2_ok = True
        else:
            n = None
            h2_ok = False
    except Exception:
        n = None
        h2_ok = False

    # H_3: k is a positive integer such that k <= n
    try:
        if n is not None:
            h3_ok = isinstance(k, int) and k >= 1 and k <= n
        else:
            h3_ok = False
    except Exception:
        h3_ok = False

    # ¬Q: The order of the group G is not exactly n(n-1)...(n-k+1)
    try:
        if n is not None and isinstance(k, int) and k >= 1:
            expected_order = math.perm(n, k)
            neg_q_ok = G.order() != expected_order
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a finite set of size n",
    "H_3: k is a positive integer such that k <= n",
    "¬Q: The order of the group G is not exactly n(n-1)...(n-k+1)"
]

N_HYP = 3
NEG_Q_INDEX = 3