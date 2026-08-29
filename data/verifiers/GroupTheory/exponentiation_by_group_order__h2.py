import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, g = witness
    except Exception:
        return [False, False]

    try:
        order = G.order()
        h1 = (order > 0) and (order != sympy.oo) and hasattr(G, 'identity')
    except Exception:
        h1 = False

    try:
        order = G.order()
        identity = G.identity
        val = g ** order
        neg_q = bool(val != identity)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: g raised to the power of the order of G is not equal to the identity element of G"
]

N_HYP = 1
NEG_Q_INDEX = 1