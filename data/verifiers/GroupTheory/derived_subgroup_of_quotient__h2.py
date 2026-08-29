import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_subgroup(N, G):
    try:
        return all(g in G for g in N.generators)
    except Exception:
        return False

def is_normal(N, G):
    try:
        if not is_subgroup(N, G):
            return False
        for g in G.generators:
            for n in N.generators:
                if (g * n * ~g) not in N:
                    return False
                if (~g * n * g) not in N:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, N = witness
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and is_subgroup(N, G)
    except Exception:
        h1 = False

    try:
        G, N = witness
        if not (isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and is_subgroup(N, G)):
            neg_q = False
        else:
            # The conclusion states that (G/N)' == G'N/N.
            # This is a well-defined true statement if and only if N is a normal subgroup of G.
            # If N is not normal, G/N is not a group, so the conclusion fails.
            neg_q = not is_normal(N, G)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group (and N is a subgroup of G)",
    "¬Q: The derived subgroup (G/N)' is not equal to G'N/N (fails because N is not normal)"
]

N_HYP = 1
NEG_Q_INDEX = 1