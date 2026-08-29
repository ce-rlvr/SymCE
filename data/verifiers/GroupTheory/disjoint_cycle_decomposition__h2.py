import sympy
from sympy.combinatorics import Permutation, Cycle
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        n, sigma = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = isinstance(n, int) and n >= 2
    except Exception:
        h1 = False
        
    try:
        # A permutation (or cycle) has a unique disjoint cycle decomposition.
        # Other objects (like integers, matrices, strings) do not.
        if isinstance(sigma, (Permutation, Cycle)):
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "¬Q: sigma cannot be uniquely expressed as a product of disjoint cycles"
]

N_HYP = 1
NEG_Q_INDEX = 1