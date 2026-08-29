import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics.permutations import Permutation
import math
import itertools
import functools

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = False
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            if hasattr(H, 'is_subgroup'):
                try:
                    h1_ok = bool(H.is_subgroup(G, strict=False))
                except TypeError:
                    h1_ok = bool(H.is_subgroup(G))
            else:
                h1_ok = all(g in G for g in H.generators)
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = False
        if isinstance(H, PermutationGroup):
            nilp = H.is_nilpotent
            if callable(nilp):
                nilp = nilp()
            neg_q_ok = not bool(nilp)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: H is not a nilpotent group"
]

N_HYP = 1
NEG_Q_INDEX = 1