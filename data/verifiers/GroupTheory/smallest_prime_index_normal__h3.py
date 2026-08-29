import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.ntheory import primefactors
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is the smallest prime number dividing the order of G",
    "H_3: The index of H in G is equal to p",
    "¬Q: H is not a normal subgroup of G"
]

def conditions(witness) -> list[bool]:
    try:
        G, H, p = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is the smallest prime number dividing the order of G
    try:
        if h1:
            factors = primefactors(G.order())
            h2 = (len(factors) > 0) and (p == min(factors))
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: The index of H in G is equal to p
    try:
        if h1:
            if isinstance(H, PermutationGroup):
                h_size = H.order()
            elif isinstance(H, (list, set, tuple)):
                h_size = len(H)
            else:
                h_size = -1
            h3 = (h_size > 0) and (G.order() == p * h_size)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: H is NOT a normal subgroup of G
    try:
        if h1:
            is_normal = False
            if isinstance(H, PermutationGroup):
                if all(g in G for g in H.generators):
                    is_normal = G.is_normal(H)
            elif isinstance(H, (list, set, tuple)):
                elements = list(H)
                if all(g in G for g in elements):
                    H_grp = PermutationGroup(elements)
                    # To be a subgroup, the generated group must have the same size as the subset
                    if H_grp.order() == len(elements):
                        is_normal = G.is_normal(H_grp)
            neg_q = not is_normal
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]