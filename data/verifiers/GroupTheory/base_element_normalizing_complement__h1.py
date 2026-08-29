import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        N, H, n = witness
    except Exception:
        return [False, False, False]
    
    try:
        if hasattr(N, 'contains'):
            h1 = bool(N.contains(n))
        elif hasattr(N, 'elements'):
            h1 = n in N.elements
        else:
            h1 = n in N
    except Exception:
        h1 = False

    try:
        if hasattr(H, 'elements'):
            H_elems = list(H.elements)
        else:
            H_elems = list(H)
    except Exception:
        H_elems = []

    try:
        n_inv = n**-1
        conj_H = [n * h * n_inv for h in H_elems]
        h2 = len(conj_H) == len(H_elems) and all(x in H_elems for x in conj_H) and all(x in conj_H for x in H_elems)
    except Exception:
        h2 = False

    try:
        n_inv = n**-1
        neg_q = any(n * h * n_inv != h for h in H_elems)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an element of N",
    "H_2: n H n^{-1} = H",
    "¬Q: For some h in H, n h n^{-1} != h"
]

N_HYP = 2
NEG_Q_INDEX = 2