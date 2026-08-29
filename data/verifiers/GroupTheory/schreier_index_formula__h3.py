import sympy
from sympy.combinatorics.free_groups import FreeGroup, FreeGroupElement
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    "H_1: F is a free group of finite rank n",
    "H_2: H is a subgroup of F",
    "¬Q: H is not a free group of rank 1 + k(n - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (F, H, n, k), (F, H, n), (F, H), or a dictionary.
    H is expected to be a list/tuple/set of FreeGroupElements representing a free basis of the subgroup.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                F, H, n, k = witness
            elif len(witness) == 3:
                F, H, n = witness
                k = None
            elif len(witness) == 2:
                F, H = witness
                n = len(F.generators) if hasattr(F, 'generators') else None
                k = None
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            F = witness.get('F')
            H = witness.get('H')
            n = witness.get('n', len(F.generators) if hasattr(F, 'generators') else None)
            k = witness.get('k', None)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F is a free group of finite rank n
    try:
        h1 = isinstance(F, FreeGroup) and len(F.generators) == n and n >= 0
    except Exception:
        h1 = False

    # H_2: H is a subgroup of F
    try:
        if isinstance(H, (list, tuple, set)):
            h2 = all(isinstance(g, FreeGroupElement) and g.group == F for g in H)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: H is NOT a free group of rank 1 + k(n - 1)
    # We assume the provided generators for H form a free basis, so rank is len(H).
    try:
        rank_H = len(H)
        if k is not None:
            neg_q = rank_H != 1 + k * (n - 1)
        else:
            # If k is not provided, check if there is NO integer k satisfying the equation
            if n - 1 != 0:
                neg_q = (rank_H - 1) % (n - 1) != 0
            else:
                neg_q = rank_H != 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]