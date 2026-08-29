import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, H = witness
        else:
            F = witness
            H = witness
    except Exception:
        return [False, False]

    try:
        if hasattr(H, 'is_subgroup'):
            is_sub = H.is_subgroup(F)
        elif hasattr(F, 'has_subgroup'):
            is_sub = F.has_subgroup(H)
        elif H == F:
            is_sub = True
        else:
            is_sub = False

        is_div = False
        if hasattr(H, 'is_divisible'):
            val = H.is_divisible
            is_div = bool(val() if callable(val) else val)
        elif hasattr(H, 'elements'):
            elements = list(H.elements)
            is_div = True
            for n in [2, 3, 5]:
                for h in elements:
                    if not any(x**n == h for x in elements):
                        is_div = False
                        break
                if not is_div:
                    break
        
        h1_ok = bool(is_sub and is_div)
    except Exception:
        h1_ok = False

    try:
        if hasattr(H, 'is_trivial'):
            val = H.is_trivial
            is_triv = bool(val() if callable(val) else val)
        elif hasattr(H, 'order'):
            val = H.order
            is_triv = (val() if callable(val) else val) == 1
        elif hasattr(H, 'elements'):
            is_triv = len(list(H.elements)) == 1
        else:
            is_triv = False
        neg_q_ok = not is_triv
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a divisible subgroup of F",
    "¬Q: H is not the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1