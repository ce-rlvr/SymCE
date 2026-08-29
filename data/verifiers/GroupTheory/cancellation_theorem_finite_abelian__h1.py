import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.group_constructs import DirectProduct
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
V4 = DirectProduct(CyclicGroup(2), CyclicGroup(2))
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
        A, B, C = witness
    except Exception:
        return [False, False, False, False]

    # H1: B is a finite abelian group
    try:
        order_B = B.order() if callable(getattr(B, 'order', None)) else B.order
        is_ab_B = B.is_abelian() if callable(getattr(B, 'is_abelian', None)) else B.is_abelian
        h1 = bool(is_ab_B) and float(order_B) < float('inf')
    except Exception:
        h1 = False

    # H2: C is a finite abelian group
    try:
        order_C = C.order() if callable(getattr(C, 'order', None)) else C.order
        is_ab_C = C.is_abelian() if callable(getattr(C, 'is_abelian', None)) else C.is_abelian
        h2 = bool(is_ab_C) and float(order_C) < float('inf')
    except Exception:
        h2 = False

    # H3: A ⊕ B is isomorphic to A ⊕ C
    try:
        if hasattr(A, 'direct_sum'):
            AB = A.direct_sum(B)
            AC = A.direct_sum(C)
        else:
            try:
                AB = A + B
                AC = A + C
            except Exception:
                AB = DirectProduct(A, B)
                AC = DirectProduct(A, C)
            
        if hasattr(AB, 'is_isomorphic'):
            h3 = bool(AB.is_isomorphic(AC))
        else:
            h3 = bool(AB == AC)
    except Exception:
        h3 = False

    # neg_Q: B is not isomorphic to C
    try:
        if hasattr(B, 'is_isomorphic'):
            neg_q = not bool(B.is_isomorphic(C))
        else:
            neg_q = bool(B != C)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: B is a finite abelian group",
    "H_2: C is a finite abelian group",
    "H_3: A ⊕ B is isomorphic to A ⊕ C",
    "¬Q: B is not isomorphic to C"
]

N_HYP = 3
NEG_Q_INDEX = 3