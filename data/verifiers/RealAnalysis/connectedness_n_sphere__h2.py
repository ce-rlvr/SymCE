import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, int):
            n = witness
        elif hasattr(witness, 'is_Integer') and witness.is_Integer:
            n = int(witness)
        else:
            n = None
    except Exception:
        n = None

    # H_1: n is an integer strictly greater than 0
    try:
        h1_ok = (n is not None) and (n > 0)
    except Exception:
        h1_ok = False

    # H_2: S^n is equipped with the subspace topology inherited from the standard topology on \mathbb{R}^{n+1}
    # This is a definitional property of the space S^n in this context.
    try:
        h2_ok = (n is not None)
    except Exception:
        h2_ok = False

    # ¬Q: S^n is NOT a connected topological space
    # S^n is connected for n >= 1. It is disconnected for n == 0 (two points) and n < 0 (empty).
    try:
        neg_q_ok = (n is not None) and (n <= 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 0",
    "H_2: S^n is equipped with the subspace topology inherited from the standard topology on R^{n+1}",
    "¬Q: S^n is not a connected topological space"
]

N_HYP = 2
NEG_Q_INDEX = 2