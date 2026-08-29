import math
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, x, y = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a nilpotent group
    try:
        if callable(G.is_nilpotent):
            h1 = bool(G.is_nilpotent())
        else:
            h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False

    # H_2: x and y are elements of G
    try:
        h2 = bool(x in G and y in G)
    except Exception:
        h2 = False

    # H_3: The order of x and the order of y are relatively prime integers
    try:
        ox = int(x.order())
        oy = int(y.order())
        h3 = bool(math.gcd(ox, oy) == 1)
    except Exception:
        h3 = False

    # ¬Q: x and y do not commute
    try:
        neg_q = bool(x * y != y * x)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: G is a nilpotent group",
    "H_2: x and y are elements of G",
    "H_3: The order of x and the order of y are relatively prime integers",
    "¬Q: x and y do not commute"
]

N_HYP: int = 3
NEG_Q_INDEX: int = 3