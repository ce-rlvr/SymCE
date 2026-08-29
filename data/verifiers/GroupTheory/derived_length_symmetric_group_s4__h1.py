import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    if isinstance(witness, tuple) and len(witness) == 2:
        n, G = witness
    else:
        G = witness
        try:
            n = G.degree
        except Exception:
            n = None

    try:
        h1 = (n == 4)
    except Exception:
        h1 = False

    try:
        if n == 4:
            # S_4 is the unique group of order 24 with a trivial center
            h2 = (G.order() == 24) and (G.center().order() == 1)
        elif isinstance(n, int) and n > 0:
            h2 = (G.order() == math.factorial(n))
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        ds = G.derived_series()
        if ds[-1].order() == 1:
            derived_length = len(ds) - 1
        else:
            derived_length = -1
        neg_q = (derived_length != 3)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n = 4",
    "H_2: G is the symmetric group S_n",
    "¬Q: The derived length of G is not exactly 3"
]

N_HYP = 2
NEG_Q_INDEX = 2