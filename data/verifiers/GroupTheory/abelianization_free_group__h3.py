import sympy
from sympy.combinatorics.free_groups import FreeGroup, free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

CONDITION_LABELS = [
    "H_1: F is a free group on a set S",
    "H_2: The cardinality of S is n",
    "¬Q: The quotient group F/F' is not isomorphic to the free abelian group of rank n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                F, n = witness
                if hasattr(F, 'is_trivial') and F.is_trivial:
                    S = []
                else:
                    try:
                        S = F.generators
                    except AttributeError:
                        S = []
            elif len(witness) == 3:
                F, S, n = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F is a free group on a set S
    try:
        if isinstance(F, FreeGroup):
            h1 = (set(S) == set(F.generators))
        elif isinstance(F, FpGroup) and len(F.relators) == 0:
            h1 = (set(S) == set(F.generators))
        elif hasattr(F, 'is_trivial') and F.is_trivial:
            h1 = (len(S) == 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: The cardinality of S is n
    try:
        h2 = (len(S) == int(n))
    except Exception:
        h2 = False

    # ¬Q: The quotient group F/F' is not isomorphic to the free abelian group of rank n
    try:
        n_int = int(n)
        if isinstance(F, FreeGroup):
            q = (len(F.generators) == n_int)
        elif hasattr(F, 'abelian_invariants'):
            q = (list(F.abelian_invariants()) == [0] * n_int)
        else:
            q = False
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]