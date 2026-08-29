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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness['F']
            S = witness['S']
            n = witness['n']
            F_prime = witness['F_prime']
        else:
            F, S, n, F_prime = witness
    except Exception:
        return [False, False, False]

    # H1: The cardinality of S is n
    try:
        h1 = (len(S) == int(n))
    except Exception:
        h1 = False

    # H2: F' is the commutator subgroup of F
    try:
        derived = F.derived_subgroup()
        if hasattr(F_prime, 'is_subgroup') and hasattr(derived, 'is_subgroup'):
            h2 = bool(F_prime.is_subgroup(derived) and derived.is_subgroup(F_prime))
        else:
            h2 = bool(F_prime == derived)
    except Exception:
        h2 = False

    # neg_Q: F/F' is NOT isomorphic to the free abelian group of rank n
    try:
        n_int = int(n)
        is_iso = False
        if hasattr(F, 'abelian_invariants'):
            invs = F.abelian_invariants()
            is_iso = (list(invs) == [0] * n_int)
        else:
            # For finite groups (like PermutationGroup), F/F' is finite.
            # The free abelian group of rank n is finite iff n == 0.
            if n_int == 0:
                is_iso = (F.order() == F_prime.order())
            else:
                is_iso = False
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The cardinality of S is n",
    "H_2: F' is the commutator subgroup of F",
    "¬Q: F/F' is not isomorphic to the free abelian group of rank n"
]

N_HYP = 2
NEG_Q_INDEX = 2