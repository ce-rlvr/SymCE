import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, x, y = witness
    except Exception:
        return [False, False, False]

    # H_1: x and y are elements of G
    try:
        h1 = bool(G.contains(x) and G.contains(y))
    except Exception:
        h1 = False

    # H_2: x and y are conjugate in G
    try:
        h2 = False
        if h1:
            for g in G.elements:
                if g * x * ~g == y:
                    h2 = True
                    break
    except Exception:
        h2 = False

    # ¬Q: x and y do NOT belong to the same left coset of the commutator subgroup in G
    try:
        neg_q = False
        if h1:
            C = G.derived_subgroup()
            # x and y are in the same left coset of C iff x^-1 * y is in C
            neg_q = not bool(C.contains(~x * y))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "H_2: x and y are conjugate in G",
    "¬Q: x and y do not belong to the same left coset of the commutator subgroup in G"
]

N_HYP = 2
NEG_Q_INDEX = 2