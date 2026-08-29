import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol
import math
import itertools
import functools
import z3

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

def is_fg(g):
    if hasattr(g, 'is_finitely_generated'):
        val = g.is_finitely_generated
        return bool(val() if callable(val) else val)
    if isinstance(g, PermutationGroup):
        return True
    if type(g).__name__ in ['FpGroup', 'FreeGroup']:
        return True
    raise ValueError("Cannot determine if finitely generated")

def has_wp(g):
    if hasattr(g, 'has_solvable_word_problem'):
        val = g.has_solvable_word_problem
        return bool(val() if callable(val) else val)
    if isinstance(g, PermutationGroup):
        return True
    if type(g).__name__ == 'FreeGroup':
        return True
    if hasattr(g, 'is_finite'):
        val = g.is_finite
        if bool(val() if callable(val) else val):
            return True
    raise ValueError("Cannot determine if word problem is solvable")

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'G') and hasattr(witness, 'H'):
            G = witness.G
            H = witness.H
        else:
            G, H = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_fg(G)
    except Exception:
        h1 = False

    try:
        h2 = has_wp(G)
    except Exception:
        h2 = False

    try:
        h3 = is_fg(H)
    except Exception:
        h3 = False

    try:
        wp_G = has_wp(G)
        wp_H = has_wp(H)
        # G x H has a solvable word problem iff both G and H do.
        # The conclusion is that G x H has a solvable word problem.
        # We want neg_Q to be True when the conclusion FAILS.
        neg_q = not (wp_G and wp_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: G has a solvable word problem",
    "H_3: H is a finitely generated group",
    "¬Q: The direct product G x H does not have a solvable word problem"
]

N_HYP = 3
NEG_Q_INDEX = 3