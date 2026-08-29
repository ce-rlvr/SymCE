import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, p, m = witness
        else:
            return [False, False, False, False, False]
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: m is a positive integer
    try:
        h2 = int(m) == m and m > 0
    except Exception:
        h2 = False

    # H_3: The order of G is pm
    try:
        h3 = G.order() == p * m
    except Exception:
        h3 = False

    # H_4: p > m
    try:
        h4 = p > m
    except Exception:
        h4 = False

    # neg_Q: The Sylow p-subgroup of G is a normal subgroup of G
    try:
        if not isprime(p):
            # If p is not prime, the concept of a Sylow p-subgroup is invalid.
            # Thus, the statement "The Sylow p-subgroup of G is a normal subgroup" is false,
            # making its negation true.
            neg_q = True
        else:
            S = G.sylow_subgroup(p)
            neg_q = not G.is_normal(S)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: m is a positive integer",
    "H_3: The order of G is pm",
    "H_4: p > m",
    "¬Q: The Sylow p-subgroup of G is not a normal subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4