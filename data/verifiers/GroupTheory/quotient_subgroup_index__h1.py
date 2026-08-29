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

def conditions(witness):
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: N is a normal subgroup of G
    try:
        if hasattr(G, 'is_normal'):
            h1 = bool(G.is_normal(N))
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h2 = bool(H.is_subgroup(G))
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: N is a subset of H
    try:
        if hasattr(N, 'is_subgroup'):
            h3 = bool(N.is_subgroup(H))
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: The index of H in G is finite
    try:
        if hasattr(G, 'index'):
            idx_GH = G.index(H)
            h4 = (idx_GH < float('inf'))
        elif hasattr(G, 'order') and hasattr(H, 'order'):
            idx_GH = sympy.Rational(G.order(), H.order())
            h4 = True
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: The index of H/N in G/N is not equal to the index of H in G
    try:
        if hasattr(G, 'index'):
            idx_GH = G.index(H)
        else:
            idx_GH = sympy.Rational(G.order(), H.order())

        if hasattr(G, 'quotient') and hasattr(H, 'quotient'):
            G_N = G.quotient(N)
            H_N = H.quotient(N)
            if hasattr(G_N, 'index'):
                idx_quotients = G_N.index(H_N)
            else:
                idx_quotients = sympy.Rational(G_N.order(), H_N.order())
        else:
            idx_G_N = sympy.Rational(G.order(), N.order())
            idx_H_N = sympy.Rational(H.order(), N.order())
            idx_quotients = sympy.Rational(idx_G_N, idx_H_N)

        neg_q = bool(idx_quotients != idx_GH)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "H_3: N is a subset of H",
    "H_4: The index of H in G is finite",
    "neg_Q: The index of H/N in G/N is not equal to the index of H in G"
]

N_HYP = 4
NEG_Q_INDEX = 4