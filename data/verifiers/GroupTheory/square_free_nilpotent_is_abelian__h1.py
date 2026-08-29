import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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
        nilp = witness.is_nilpotent
        if callable(nilp):
            nilp = nilp()
        h1 = bool(nilp)
    except Exception:
        h1 = False

    try:
        order = witness.order
        if callable(order):
            order = order()
        factors = factorint(order)
        h2 = all(v == 1 for v in factors.values())
    except Exception:
        h2 = False

    try:
        ab = witness.is_abelian
        if callable(ab):
            ab = ab()
        neg_q = not bool(ab)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: The order of G is a square-free integer",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2