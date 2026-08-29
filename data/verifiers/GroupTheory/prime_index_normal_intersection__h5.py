import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools
import z3

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        G, N, H, p = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        if not isinstance(N, PermutationGroup):
            h2 = False
        else:
            h2 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h2 = False

    # H3: p is a prime number
    try:
        h3 = bool(isprime(p))
    except Exception:
        h3 = False

    # H4: Index of N in G is p
    try:
        h4 = bool(G.order() == p * N.order())
    except Exception:
        h4 = False

    # neg_Q: Either H is a subset of N or index of H intersect N in H is p (Negated)
    try:
        def canonical_perm(perm):
            if not hasattr(perm, 'array_form'):
                return perm
            arr = list(perm.array_form)
            while arr and arr[-1] == len(arr) - 1:
                arr.pop()
            return tuple(arr)

        if hasattr(H, 'elements'):
            H_els = {canonical_perm(x) for x in H.elements}
        else:
            H_els = {canonical_perm(x) for x in H}

        if hasattr(N, 'elements'):
            N_els = {canonical_perm(x) for x in N.elements}
        else:
            N_els = {canonical_perm(x) for x in N}

        H_cap_N_els = H_els.intersection(N_els)

        H_cap_N_order = len(H_cap_N_els)
        H_order = len(H_els)

        is_sub = H_els.issubset(N_els)

        if H_cap_N_order == 0:
            idx_eq_p = False
        else:
            idx_eq_p = (H_order == p * H_cap_N_order)

        q = is_sub or idx_eq_p
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: p is a prime number",
    "H_4: Index of N in G is p",
    "¬Q: H is not a subset of N and index of H intersect N in H is not p"
]

N_HYP = 4
NEG_Q_INDEX = 4