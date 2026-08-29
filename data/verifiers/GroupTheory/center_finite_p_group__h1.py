import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math
import itertools
import functools

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
    # H_1: The order of G is p^n for some prime p and integer n >= 1
    try:
        order = witness.order()
        if order <= 1 or order == sympy.oo:
            h1_ok = False
        else:
            factors = factorint(order)
            h1_ok = (len(factors) == 1)
    except Exception:
        h1_ok = False

    # neg_Q: The center Z(G) is trivial (order 1)
    try:
        if hasattr(witness, 'center'):
            c = witness.center()
            if hasattr(c, 'order'):
                neg_q_ok = bool(c.order() == 1)
            else:
                neg_q_ok = bool(len(c) == 1)
        else:
            elements = list(witness.generate())
            center_size = sum(1 for g in elements if all(g*h == h*g for h in elements))
            neg_q_ok = bool(center_size == 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The order of G is p^n for some prime p and integer n >= 1",
    "¬Q: The center Z(G) is trivial"
]

N_HYP = 1
NEG_Q_INDEX = 1