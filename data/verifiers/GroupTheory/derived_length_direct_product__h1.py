import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics.permutations import Permutation
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

def is_solvable_group(grp):
    solv = grp.is_solvable
    if callable(solv):
        return solv()
    return solv

def get_derived_length(grp):
    if not is_solvable_group(grp):
        raise ValueError("Derived length is undefined for non-solvable groups.")
    ds = grp.derived_series
    if callable(ds):
        ds = ds()
    return len(ds) - 1

def direct_product(G, H):
    n = G.degree
    if n == 0: n = 1
    m = H.degree
    if m == 0: m = 1
    gens = []
    for g in G.generators:
        arr = g.array_form
        if len(arr) < n:
            arr = arr + list(range(len(arr), n))
        arr = arr + list(range(n, n + m))
        gens.append(Permutation(arr))
    for h in H.generators:
        arr = h.array_form
        if len(arr) < m:
            arr = arr + list(range(len(arr), m))
        arr = list(range(n)) + [x + n for x in arr]
        gens.append(Permutation(arr))
    if not gens:
        return PermutationGroup([Permutation(n + m - 1)])
    return PermutationGroup(*gens)

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: H is a solvable group
    try:
        h1_ok = bool(is_solvable_group(H))
    except Exception:
        h1_ok = False

    # neg_Q: The derived length of G x H is not equal to max(d(G), d(H))
    try:
        d_G = get_derived_length(G)
        d_H = get_derived_length(H)
        
        GxH = direct_product(G, H)
        d_GxH = get_derived_length(GxH)
        
        conclusion = (d_GxH == max(d_G, d_H))
        neg_q_ok = not conclusion
    except Exception:
        # If derived length is undefined (e.g., G is not solvable), the conclusion fails.
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a solvable group",
    "¬Q: The derived length of G x H is not equal to max(d(G), d(H)) (or is undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1