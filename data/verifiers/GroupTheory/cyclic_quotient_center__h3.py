import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
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
    if isinstance(witness, tuple) and len(witness) == 2:
        G, Z = witness
    else:
        G = witness
        try:
            Z = G.center()
        except Exception:
            Z = None

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if h1 and Z is not None:
            C = G.center()
            h2 = bool(Z.is_subgroup(C) and C.is_subgroup(Z))
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        neg_q = not bool(G.is_abelian)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Z(G) is the center of G",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2