import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
from sympy import abc
from sympy.polys import *
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
V4 = AlternatingGroup(4) # V4 is isomorphic to a subgroup of A4, but we'll leave it as A4 for simplicity if needed
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: The order of G is 56",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # H_1: The order of G is 56
    try:
        h1_ok = bool(witness.order() == 56)
    except Exception:
        h1_ok = False

    # ¬Q: G is not a solvable group
    try:
        neg_q_ok = not bool(witness.is_solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]