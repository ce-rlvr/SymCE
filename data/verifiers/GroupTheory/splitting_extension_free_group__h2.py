import itertools
import math
import functools
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.abc

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

def conditions(witness) -> list[bool]:
    """
    Given a witness object (expected to be a tuple (G, N) where G is a group and N is a subgroup),
    checks the remaining hypotheses and the negated conclusion.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        if hasattr(G, 'is_group'):
            h1_ok = bool(G.is_group())
        else:
            h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: The quotient group G/N is a free group
    try:
        if hasattr(G, 'quotient_is_free'):
            h2_ok = bool(G.quotient_is_free(N))
        else:
            if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
                if N.is_subgroup(G) and N.is_normal(G):
                    # For finite groups, the only free group is the trivial group
                    h2_ok = (G.order() == N.order())
                else:
                    h2_ok = False
            else:
                h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The short exact sequence 1 -> N -> G -> G/N -> 1 splits, implying G is isomorphic to N ⋊ (G/N)
    # Negation: The sequence does NOT split.
    try:
        if hasattr(G, 'splits_over'):
            neg_q = not bool(G.splits_over(N))
        else:
            if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
                if N.is_subgroup(G) and N.is_normal(G) and G.order() == N.order():
                    # If G/N is trivial, G is isomorphic to N, so it trivially splits.
                    neg_q = False
                else:
                    neg_q = False
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The quotient group G/N is a free group",
    "¬Q: The short exact sequence 1 -> N -> G -> G/N -> 1 does not split"
]

N_HYP = 2
NEG_Q_INDEX = 2