import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to be the degree n of the symmetric group
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            h1_ok = n >= 1
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    try:
        if h1_ok:
            G = SymmetricGroup(int(witness))
            # The conclusion is that S_n is not solvable.
            # The negated conclusion is that S_n IS solvable.
            neg_q_ok = bool(G.is_solvable)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: S_n is solvable"
]

N_HYP = 1
NEG_Q_INDEX = 1
