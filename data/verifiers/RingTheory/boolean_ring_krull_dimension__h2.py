import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Let R be a Boolean ring.
    try:
        h1 = False
        if hasattr(witness, 'is_boolean_ring'):
            val = witness.is_boolean_ring
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_Boolean_ring'):
            val = witness.is_Boolean_ring
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'elements') and hasattr(witness, 'mul'):
            h1 = True
            for x in witness.elements:
                if witness.mul(x, x) != x:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: Let R be non-trivial (1 != 0).
    try:
        h2 = False
        if hasattr(witness, 'is_nontrivial'):
            val = witness.is_nontrivial
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_non_trivial'):
            val = witness.is_non_trivial
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'one') and hasattr(witness, 'zero'):
            h2 = bool(witness.one != witness.zero)
    except Exception:
        h2 = False

    # ¬Q: The Krull dimension of R is not 0.
    try:
        neg_q = False
        if hasattr(witness, 'krull_dimension'):
            val = witness.krull_dimension
            neg_q = bool((val() if callable(val) else val) != 0)
        elif hasattr(witness, 'krull_dim'):
            val = witness.krull_dim
            neg_q = bool((val() if callable(val) else val) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R is non-trivial (1 != 0)",
    "¬Q: The Krull dimension of R is not 0"
]

N_HYP = 2
NEG_Q_INDEX = 2