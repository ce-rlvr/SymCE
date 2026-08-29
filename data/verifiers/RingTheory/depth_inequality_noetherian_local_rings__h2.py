import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    # H_1: R is a commutative Noetherian local ring
    try:
        if isinstance(witness, dict):
            is_comm = witness.get('is_commutative', False)
            is_noeth = witness.get('is_noetherian', False)
            is_local = witness.get('is_local', False)
        else:
            is_comm = getattr(witness, 'is_commutative', False)
            is_noeth = getattr(witness, 'is_noetherian', False)
            is_local = getattr(witness, 'is_local', False)
        h1 = bool(is_comm and is_noeth and is_local)
    except Exception:
        h1 = False

    # ¬Q: The depth of R with respect to \mathfrak{m} is greater than the Krull dimension of R
    try:
        if isinstance(witness, dict):
            depth = witness.get('depth', 0)
            dim = witness.get('krull_dimension', 0)
        else:
            depth = getattr(witness, 'depth', 0)
            dim = getattr(witness, 'krull_dimension', 0)
        neg_q = bool(depth > dim)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian local ring",
    "¬Q: The depth of R with respect to m is greater than the Krull dimension of R"
]

N_HYP = 1
NEG_Q_INDEX = 1