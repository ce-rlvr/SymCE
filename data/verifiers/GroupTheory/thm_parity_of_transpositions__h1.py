import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        # H_1: Let \tau \in S_n be a transposition
        # A transposition is a permutation that moves exactly 2 elements.
        h1 = isinstance(witness, Permutation) and len(witness.support()) == 2
    except Exception:
        h1 = False

    try:
        # Conclusion: \tau is an odd permutation
        # Negated conclusion: \tau is an even permutation (sign is 1)
        neg_q = witness.is_even == True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: tau is a transposition in S_n",
    "¬Q: tau is an even permutation"
]

N_HYP = 1
NEG_Q_INDEX = 1