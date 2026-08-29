import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: G is the dihedral group D_{2n} of order 2n
    h1_ok = False
    try:
        if hasattr(witness, 'order') and hasattr(witness, 'elements'):
            order = witness.order()
            if order % 2 == 0:
                n = order // 2
                if n >= 1:
                    elements = list(witness.elements)
                    r_cands = [x for x in elements if x.order() == n]
                    s_cands = [x for x in elements if x.order() == 2]
                    for r in r_cands:
                        r_inv = r**-1
                        r_powers = [r**i for i in range(n)]
                        for s in s_cands:
                            if s not in r_powers:
                                if s * r * s == r_inv:
                                    h1_ok = True
                                    break
                        if h1_ok:
                            break
    except Exception:
        h1_ok = False

    # neg_Q: The center Z(G) does not have exactly 2 elements
    neg_q_ok = False
    try:
        if hasattr(witness, 'center'):
            c_order = witness.center().order()
            neg_q_ok = (c_order != 2)
        elif hasattr(witness, 'elements'):
            elements = list(witness.elements)
            c_order = sum(1 for x in elements if all(x * y == y * x for y in elements))
            neg_q_ok = (c_order != 2)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is the dihedral group D_{2n} of order 2n",
    "¬Q: The center Z(G) does not have exactly 2 elements"
]

N_HYP = 1
NEG_Q_INDEX = 1