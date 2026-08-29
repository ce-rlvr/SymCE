import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    # H_1: G is the dihedral group D_{2n} of order 2n
    try:
        order = witness.order()
        if order % 2 != 0:
            h1 = False
        else:
            n = order // 2
            if n < 1:
                h1 = False
            else:
                elements = list(witness.generate())
                if n == 1:
                    h1 = (order == 2)
                elif n == 2:
                    h1 = (order == 4 and all(g.order() in (1, 2) for g in elements))
                else:
                    h1 = False
                    for x in elements:
                        if x.order() == n:
                            x_inv = x**(-1)
                            for y in elements:
                                if y.order() == 2:
                                    if y * x * y == x_inv:
                                        h1 = True
                                        break
                            if h1:
                                break
    except Exception:
        h1 = False

    # neg_Q: The center Z(G) is not the trivial subgroup
    try:
        elements = list(witness.generate())
        center_size = sum(1 for g in elements if all(g * h == h * g for h in elements))
        neg_q = (center_size > 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the dihedral group D_{2n} of order 2n",
    "¬Q: The center Z(G) is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1