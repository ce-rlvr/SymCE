import math
import itertools
import functools
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import z3

# Top-level setup: named object bindings
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
    # H_1: G is the symmetric group S_n
    try:
        if not isinstance(witness, PermutationGroup):
            h1 = False
        else:
            n = witness.degree
            h1 = bool(n >= 1 and witness.order() == math.factorial(n))
    except Exception:
        h1 = False

    # ¬Q: G is not a solvable group
    try:
        solvable = witness.is_solvable
        if callable(solvable):
            solvable = solvable()
        neg_q = not bool(solvable)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the symmetric group S_n",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1