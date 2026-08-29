import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                F, H, n, k = witness
            elif len(witness) == 3:
                F, H, k = witness
                n = len(F.generators)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: H is a subgroup of F
    try:
        h1 = bool(H.is_subgroup(F))
    except Exception:
        h1 = False

    # H2: The index of H in F is a finite integer k
    try:
        oF_attr = getattr(F, 'order', None)
        oF = oF_attr() if callable(oF_attr) else oF_attr
        
        oH_attr = getattr(H, 'order', None)
        oH = oH_attr() if callable(oH_attr) else oH_attr
        
        if oF is not None and oH is not None and oF != 0 and oH != 0:
            if oF % oH == 0:
                idx = oF // oH
                h2 = bool(idx == k)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: H is NOT a free group of finite rank equal to 1 + k(n - 1)
    try:
        is_free = False
        rank = None
        
        oH_attr = getattr(H, 'order', None)
        oH = oH_attr() if callable(oH_attr) else oH_attr
        
        if oH == 1:
            is_free = True
            rank = 0
        elif type(H).__name__ == 'FreeGroup':
            is_free = True
            rank = len(H.generators)
        elif hasattr(H, 'relators') and len(H.relators) == 0:
            is_free = True
            rank = len(H.generators)
            
        if is_free and rank is not None:
            expected_rank = 1 + k * (n - 1)
            q = bool(rank == expected_rank)
        else:
            q = False
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of F",
    "H_2: The index of H in F is a finite integer k",
    "¬Q: H is not a free group of finite rank equal to 1 + k(n - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2