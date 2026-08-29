import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

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

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, x = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = G.contains(x) and x != G.identity
    except Exception:
        h2 = False

    try:
        x_inv = x**-1
        neg_q = any(g * x * g**-1 == x_inv for g in G.elements)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x is an element of G such that x is not the identity element",
    "¬Q: x is conjugate to x^(-1) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2