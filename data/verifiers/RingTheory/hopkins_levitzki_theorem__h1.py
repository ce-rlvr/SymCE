import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
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
    # H_1: R has a multiplicative identity
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('has_multiplicative_identity', witness.get('has_identity', witness.get('is_unital', False))))
        else:
            h1 = bool(getattr(witness, 'has_multiplicative_identity', getattr(witness, 'has_identity', getattr(witness, 'is_unital', False))))
    except Exception:
        h1 = False

    # H_2: R is a left Artinian ring
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('is_left_artinian', witness.get('is_artinian', False)))
        else:
            h2 = bool(getattr(witness, 'is_left_artinian', getattr(witness, 'is_artinian', False)))
    except Exception:
        h2 = False

    # ¬Q: R is not a left Noetherian ring
    try:
        if isinstance(witness, dict):
            q = bool(witness.get('is_left_noetherian', witness.get('is_noetherian', True)))
        else:
            q = bool(getattr(witness, 'is_left_noetherian', getattr(witness, 'is_noetherian', True)))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R has a multiplicative identity",
    "H_2: R is a left Artinian ring",
    "¬Q: R is not a left Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2