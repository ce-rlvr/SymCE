import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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
    # H_1: The rank of F is strictly greater than 1
    try:
        h1 = False
        if hasattr(witness, 'rank'):
            r = witness.rank
            if callable(r):
                r = r()
            h1 = int(r) > 1
        elif hasattr(witness, 'is_cyclic'):
            is_cyc = witness.is_cyclic
            if callable(is_cyc):
                is_cyc = is_cyc()
            order = witness.order
            if callable(order):
                order = order()
            # For finite groups, rank > 1 is equivalent to being non-cyclic and non-trivial
            h1 = (not is_cyc) and (int(order) > 1)
    except Exception:
        h1 = False

    # neg_Q: F is a solvable group (negation of "F is not a solvable group")
    try:
        neg_q = False
        if hasattr(witness, 'is_solvable'):
            s = witness.is_solvable
            if callable(s):
                s = s()
            neg_q = bool(s)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The rank of F is strictly greater than 1",
    "¬Q: F is a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1