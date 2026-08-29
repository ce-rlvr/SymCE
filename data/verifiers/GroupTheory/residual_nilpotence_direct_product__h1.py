import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def check_nilpotent(grp):
    val = grp.is_nilpotent
    if callable(val):
        return val()
    return val

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
        else:
            G = witness.G
            H = witness.H
    except Exception:
        return [False, False]

    try:
        h1 = bool(check_nilpotent(H))
    except Exception:
        h1 = False

    try:
        # For finite groups, the direct product G x H is residually nilpotent 
        # (which is equivalent to nilpotent) if and only if both G and H are nilpotent.
        g_x_h_nilpotent = bool(check_nilpotent(G) and check_nilpotent(H))
        neg_q = not g_x_h_nilpotent
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a residually nilpotent group",
    "¬Q: The direct product G x H is not a residually nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1
