import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import totient

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
        if isinstance(witness, tuple):
            if len(witness) == 3:
                G, n, d = witness
            elif len(witness) == 2:
                G, d = witness
                n = G.order()
            else:
                G, n, d = None, None, None
        else:
            G, n, d = None, None, None
    except Exception:
        G, n, d = None, None, None

    try:
        h1 = (int(d) == d) and (d > 0)
    except Exception:
        h1 = False

    try:
        h2 = (int(n) == n) and (n > 0) and (n % d == 0) and (G.order() == n)
    except Exception:
        h2 = False

    try:
        expected = totient(int(d))
        actual = sum(1 for g in G.elements if g.order() == d)
        neg_q = actual != expected
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: d is a positive integer",
    "H_2: d divides n",
    "¬Q: G does not contain exactly phi(d) elements of order d"
]

N_HYP = 2
NEG_Q_INDEX = 2