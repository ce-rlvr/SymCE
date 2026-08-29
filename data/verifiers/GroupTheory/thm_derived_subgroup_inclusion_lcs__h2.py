import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
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
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_derived_term(G, k):
    ds = G.derived_series()
    if k < len(ds):
        return ds[k]
    return ds[-1]

def get_lower_central_term(G, n):
    lcs = G.lower_central_series()
    if n - 1 < len(lcs):
        return lcs[n - 1]
    return lcs[-1]

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, k = witness
        else:
            G = witness
            k = None
    except Exception:
        G = witness
        k = None

    # H_1: G is a group
    try:
        h1 = hasattr(G, 'generators') and hasattr(G, 'contains')
    except Exception:
        h1 = False

    # neg_Q: The k-th derived subgroup G^(k) is NOT a subgroup of gamma_{2^k}(G)
    try:
        if k is not None:
            if not isinstance(k, int) or k < 0:
                neg_q = False
            else:
                G_k = get_derived_term(G, k)
                gamma_2k = get_lower_central_term(G, 2**k)
                neg_q = not all(g in gamma_2k for g in G_k.generators)
        else:
            ds = G.derived_series()
            neg_q = False
            for i in range(len(ds)):
                G_i = ds[i]
                gamma_2i = get_lower_central_term(G, 2**i)
                if not all(g in gamma_2i for g in G_i.generators):
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The k-th derived subgroup G^(k) is not a subgroup of gamma_{2^k}(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1