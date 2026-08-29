import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
from sympy import abc
from sympy.polys import *

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    # H_1: G is a permutation group (subgroup of S_p)
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G acts transitively on its domain
    try:
        h2 = False
        if h1:
            if callable(witness.is_transitive):
                h2 = bool(witness.is_transitive())
            else:
                h2 = bool(witness.is_transitive)
    except Exception:
        h2 = False

    # H_3: G contains at least one transposition
    try:
        h3 = False
        if h1:
            for i, g in enumerate(witness.generate()):
                if i > 10000:  # Prevent infinite loops or excessive time on huge groups
                    break
                # A transposition has exactly one cycle of length 2, and all other elements are fixed
                cycles = [c for c in g.cyclic_form if len(c) > 1]
                if len(cycles) == 1 and len(cycles[0]) == 2:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # ¬Q: G is not equal to the symmetric group S_p
    try:
        neg_q = False
        if h1:
            n = witness.degree
            if n <= 1000:  # Prevent factorial of excessively large numbers
                # If G is a subgroup of S_n, it is equal to S_n iff its order is n!
                neg_q = witness.order() < math.factorial(n)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a permutation group",
    "H_2: G acts transitively on its domain",
    "H_3: G contains at least one transposition",
    "¬Q: G is not equal to the symmetric group on its domain"
]

N_HYP = 3
NEG_Q_INDEX = 3