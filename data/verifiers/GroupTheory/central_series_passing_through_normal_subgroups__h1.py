import sympy
import sympy.combinatorics
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False]
        
    # H_1: N is a normal subgroup of G
    try:
        is_subgroup = all(G.contains(n) for n in N.generators)
        is_normal = True
        if is_subgroup:
            for g in G.generators:
                for n in N.generators:
                    # Check conjugation in both directions to be independent of multiplication convention
                    if not N.contains(g * n * ~g) or not N.contains(~g * n * g):
                        is_normal = False
                        break
                if not is_normal:
                    break
        h1 = is_subgroup and is_normal
    except Exception:
        h1 = False

    # ¬Q: There does NOT exist a central series of G that includes N as one of its terms.
    # A central series of G passing through N exists if and only if G is nilpotent.
    # (If G is nilpotent, N_i = N \cap Z_i(G) and W_j/N = Z_j(G/N) form such a series.
    # If G is not nilpotent, it has no central series at all.)
    # Thus, the conclusion fails (neg_q is True) iff G is NOT nilpotent.
    try:
        nilpotent = G.is_nilpotent
        if callable(nilpotent):
            nilpotent = nilpotent()
        neg_q = not nilpotent
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: There does not exist a central series of G that includes N as one of its terms"
]

N_HYP = 1
NEG_Q_INDEX = 1