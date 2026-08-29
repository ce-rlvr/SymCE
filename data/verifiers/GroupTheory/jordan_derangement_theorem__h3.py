import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    try:
        h3 = isinstance(witness, PermutationGroup) and bool(witness.is_transitive)
    except Exception:
        h3 = False

    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        elif witness.order() > 2000:
            neg_q = False
        else:
            deg = witness.degree
            # An element g has no fixed points iff it moves all 'deg' elements (len(g.support()) == deg).
            # The negation of the conclusion is that ALL elements have at least one fixed point,
            # which means len(g.support()) < deg for all g in G.
            neg_q = all(len(g.support()) < deg for g in witness.elements)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: X is a finite set",
    "H_3: The action of G on X is transitive",
    "¬Q: For all g in G, g has at least one fixed point in X"
]

N_HYP = 3
NEG_Q_INDEX = 3