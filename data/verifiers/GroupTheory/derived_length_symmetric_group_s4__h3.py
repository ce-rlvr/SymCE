import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
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
    # Parse witness: could be a tuple (n, G) or just a group G
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, G = witness
        else:
            G = witness
            n = getattr(G, 'degree', 4)
    except Exception:
        n, G = None, None

    # H_1: n is an integer
    try:
        h1_ok = isinstance(n, int)
    except Exception:
        h1_ok = False

    # H_2: n = 4
    try:
        h2_ok = (n == 4)
    except Exception:
        h2_ok = False

    # ¬Q: The derived length of G is NOT exactly 3
    try:
        ds = G.derived_series()
        is_solvable = (ds[-1].order() == 1)
        if is_solvable:
            dl = len(ds) - 1
        else:
            dl = float('inf')
        neg_q_ok = (dl != 3)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: n = 4",
    "¬Q: The derived length of G is not exactly 3"
]

N_HYP = 2
NEG_Q_INDEX = 2