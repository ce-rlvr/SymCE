import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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

def conditions(witness) -> list[bool]:
    try:
        n, F, F_prime = witness
    except Exception:
        return [False, False, False]

    # H_1: n is greater than or equal to 2
    try:
        h1 = int(n) >= 2
    except Exception:
        h1 = False

    # H_2: F' is the commutator subgroup of F
    try:
        derived = F.derived_subgroup()
        if F_prime == derived:
            h2 = True
        elif hasattr(F_prime, 'is_subgroup') and hasattr(derived, 'is_subgroup'):
            h2 = bool(F_prime.is_subgroup(derived) and derived.is_subgroup(F_prime))
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: F' is not a free group of countably infinite rank
    try:
        # Any finite group or finitely generated free group in SymPy 
        # is not a free group of countably infinite rank.
        if hasattr(F_prime, 'order') or hasattr(F_prime, 'generators'):
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is greater than or equal to 2",
    "H_2: F' is the commutator subgroup of F",
    "¬Q: F' is not a free group of countably infinite rank"
]

N_HYP = 2
NEG_Q_INDEX = 2