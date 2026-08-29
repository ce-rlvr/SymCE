import math
import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        if hasattr(witness, 'order'):
            order = witness.order() if callable(witness.order) else witness.order
            order = int(order)
            if order > 0:
                root = int(math.isqrt(order))
                h1 = (root * root == order)
            else:
                h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'is_abelian'):
            is_ab = witness.is_abelian() if callable(witness.is_abelian) else witness.is_abelian
            neg_q = not bool(is_ab)
        elif hasattr(witness, 'center'):
            c = witness.center()
            c_order = c.order() if callable(c.order) else c.order
            g_order = witness.order() if callable(witness.order) else witness.order
            neg_q = int(c_order) != int(g_order)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group of order p^2",
    "¬Q: The center Z(G) is not equal to G"
]

N_HYP = 1
NEG_Q_INDEX = 1