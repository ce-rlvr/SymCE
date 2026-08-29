import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        return [False, False, False]
    
    # H1: N is a normal subgroup of G
    try:
        h1 = True
        # Check if N is a subgroup of G
        if not all(G.contains(n) for n in N.generators):
            h1 = False
        else:
            # Check normality: g * n * g^-1 in N for all generators g of G and n of N
            for g in G.generators:
                for n in N.generators:
                    if not N.contains(g * n * ~g):
                        h1 = False
                        break
                    if not N.contains(~g * n * g):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: The intersection of N and the commutator subgroup is the trivial subgroup
    try:
        h2 = True
        D = G.derived_subgroup()
        for n in N.elements:
            if getattr(n, 'is_Identity', False) or n == G.identity:
                continue
            if D.contains(n):
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: N is NOT contained in the center Z(G)
    try:
        neg_q = False
        # If any generator of N does not commute with any generator of G, N is not in Z(G)
        for n in N.generators:
            for g in G.generators:
                if n * g != g * n:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The intersection of N and the commutator subgroup is the trivial subgroup",
    "not Q: N is not contained in the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2