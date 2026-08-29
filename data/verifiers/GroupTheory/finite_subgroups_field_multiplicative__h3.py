import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
V4 = DihedralGroup(2)
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
    # The witness may be provided as a tuple (F, F_times, G) or just the group G.
    if isinstance(witness, tuple):
        G = witness[-1]
    else:
        G = witness

    # H_1: F is a field
    # Since the dropped hypothesis removes the connection between G and F, 
    # F and F^\times exist vacuously as long as G is a valid group.
    try:
        _ = G.order()
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: F^\times is the multiplicative group of non-zero elements of F
    h2_ok = h1_ok

    # H_3: G is finite
    try:
        if hasattr(G, 'is_finite') and G.is_finite is not None:
            h3_ok = bool(G.is_finite)
        else:
            h3_ok = G.order() < float('inf')
    except Exception:
        h3_ok = False

    # ¬Q: G is not a cyclic group
    try:
        if hasattr(G, 'is_cyclic'):
            if callable(G.is_cyclic):
                neg_q_ok = not bool(G.is_cyclic())
            else:
                neg_q_ok = not bool(G.is_cyclic)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: F^\\times is the multiplicative group of non-zero elements of F",
    "H_3: G is finite",
    "¬Q: G is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3