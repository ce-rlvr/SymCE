import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
        A, B, G = witness
    except Exception:
        return [False, False, False]

    try:
        h1_val = getattr(A, 'is_solvable', False)
        h1 = h1_val() if callable(h1_val) else h1_val
    except Exception:
        h1 = False

    try:
        h2_val = getattr(B, 'is_solvable', False)
        h2 = h2_val() if callable(h2_val) else h2_val
    except Exception:
        h2 = False

    try:
        if not hasattr(G, 'is_solvable'):
            neg_q = False
        else:
            q_val = getattr(G, 'is_solvable')
            q = q_val() if callable(q_val) else q_val
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a finite solvable group",
    "H_2: B is a finite solvable group",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2