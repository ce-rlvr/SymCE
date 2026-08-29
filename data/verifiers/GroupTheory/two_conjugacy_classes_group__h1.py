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
        if callable(witness.conjugacy_classes):
            classes = witness.conjugacy_classes()
        else:
            classes = witness.conjugacy_classes
        h1 = len(classes) == 2
    except Exception:
        h1 = False

    try:
        is_iso = None
        if hasattr(witness, 'is_isomorphic'):
            try:
                is_iso = witness.is_isomorphic(Z2)
            except Exception:
                pass
        
        if is_iso is None and hasattr(witness, 'order'):
            try:
                if callable(witness.order):
                    w_order = witness.order()
                else:
                    w_order = witness.order
                is_iso = (w_order == 2)
            except Exception:
                pass
                
        if is_iso is None:
            is_iso = False
            
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G has exactly two distinct conjugacy classes",
    "¬Q: G is not isomorphic to the cyclic group of order 2"
]

N_HYP = 1
NEG_Q_INDEX = 1