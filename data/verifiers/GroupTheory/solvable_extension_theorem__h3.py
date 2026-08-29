import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G and N are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        if h1:
            is_sub = all(G.contains(n) for n in N.generators)
            is_norm = all(N.contains(g * n * ~g) for n in N.generators for g in G.generators)
            h2 = bool(is_sub and is_norm)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: G/N is a solvable group
    try:
        if h1 and h2:
            h3 = False
            for H in G.derived_series():
                if all(N.contains(g) for g in H.generators):
                    h3 = True
                    break
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: G is not a solvable group
    try:
        if h1:
            neg_q = not bool(G.is_solvable)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and N are groups",
    "H_2: N is a normal subgroup of G",
    "H_3: G/N is a solvable group",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3