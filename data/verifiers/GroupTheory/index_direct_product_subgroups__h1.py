import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
        A, B, H, K = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = H.is_subgroup(A)
        if h1:
            idx_A_H = A.order() / H.order()
            if idx_A_H == float('inf'):
                h1 = False
    except Exception:
        h1 = False

    try:
        h2 = K.is_subgroup(B)
        if h2:
            idx_B_K = B.order() / K.order()
            if idx_B_K == float('inf'):
                h2 = False
    except Exception:
        h2 = False

    try:
        idx_A_H = A.order() // H.order()
        idx_B_K = B.order() // K.order()
        expected_idx = idx_A_H * idx_B_K
        
        AxB = A * B
        HxK = H * K
        
        actual_idx = AxB.order() // HxK.order()
        
        is_sub = H.is_subgroup(A) and K.is_subgroup(B)
        
        concl = is_sub and (actual_idx == expected_idx)
        neg_q = not concl
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a subgroup of A with finite index",
    "H_2: K is a subgroup of B with finite index",
    "not Q: The direct product H x K is not a subgroup of A x B, or its index is not the product of their indices"
]

N_HYP = 2
NEG_Q_INDEX = 2