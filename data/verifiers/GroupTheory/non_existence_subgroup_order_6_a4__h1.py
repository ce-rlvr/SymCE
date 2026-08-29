import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # Safely extract a set of elements from the witness
    try:
        if hasattr(witness, 'generate'):
            H_set = set(witness.generate())
        else:
            H_set = set(witness)
    except Exception:
        H_set = set()

    # H_1: H is a subset of A_4
    try:
        A4_set = set(A4.generate())
        h1 = H_set.issubset(A4_set)
    except Exception:
        h1 = False

    # H_2: The cardinality of H is 6
    try:
        h2 = len(H_set) == 6
    except Exception:
        h2 = False

    # neg_Q: H is a subgroup of A_4
    try:
        A4_set = set(A4.generate())
        if not H_set:
            neg_q = False
        elif not H_set.issubset(A4_set):
            neg_q = False
        else:
            # Check closure under multiplication
            neg_q = all((x * y) in H_set for x in H_set for y in H_set)
            # Check closure under inverses
            if neg_q:
                neg_q = all((x**-1) in H_set for x in H_set)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subset of A_4",
    "H_2: The cardinality of H is 6",
    "¬Q: H is a subgroup of A_4"
]

N_HYP = 2
NEG_Q_INDEX = 2