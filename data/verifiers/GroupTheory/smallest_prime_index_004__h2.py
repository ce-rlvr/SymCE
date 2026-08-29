import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
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
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G of index p
    try:
        is_sub = True
        if h1:
            for h in H.generators:
                if not G.contains(h):
                    is_sub = False
                    break
        else:
            is_sub = False
        
        if is_sub:
            order_G = G.order()
            order_H = H.order()
            if order_G % order_H == 0:
                index = order_G // order_H
                h2 = isprime(index)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: H is not a normal subgroup of G
    try:
        if h1:
            is_norm = True
            for g in G.generators:
                for h in H.generators:
                    if not H.contains(g * h * g**-1):
                        is_norm = False
                        break
                if not is_norm:
                    break
            neg_q = not is_norm
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G of index p",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2