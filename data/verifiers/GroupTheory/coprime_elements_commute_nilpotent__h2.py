import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(x, Permutation) and isinstance(y, Permutation) and (x in G) and (y in G)
    except Exception:
        h2 = False

    try:
        h3 = math.gcd(int(x.order()), int(y.order())) == 1
    except Exception:
        h3 = False

    try:
        neg_q = (x * y) != (y * x)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x and y are elements of G",
    "H_3: The order of x and the order of y are relatively prime integers",
    "¬Q: x and y do not commute"
]

N_HYP = 3
NEG_Q_INDEX = 3