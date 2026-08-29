import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            Z = witness.center()
            q_order = witness.order() // Z.order()
            if q_order == 1:
                h2 = True
            else:
                Z_elements = set(Z.generate())
                h2 = False
                for g in witness.generate():
                    k = 1
                    curr = g
                    while curr not in Z_elements:
                        curr = curr * g
                        k += 1
                    if k == q_order:
                        h2 = True
                        break
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The quotient group G/Z(G) is a cyclic group",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2