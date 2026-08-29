import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            order = witness.order()
            if order % 17 != 0:
                neg_q = False
            else:
                P = witness.sylow_subgroup(17)
                is_norm = True
                for g in witness.generators:
                    g_inv = ~g
                    for h in P.generators:
                        if (g * h * g_inv) not in P:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                neg_q = not is_norm
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G does not have a unique, normal Sylow 17-subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1