import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import *
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
    # H_1: The order of G is 168
    try:
        h1 = (witness.order() == 168)
    except Exception:
        h1 = False

    # ¬Q: The number of Sylow 7-subgroups of G is not exactly 8
    try:
        if hasattr(witness, 'order') and callable(witness.order):
            order = witness.order()
            if order <= 5000:
                if hasattr(witness, 'elements'):
                    elements = witness.elements
                else:
                    elements = list(witness.generate())
                
                count_7 = 0
                for g in elements:
                    try:
                        o = g.order()
                    except TypeError:
                        o = g.order
                    if o == 7:
                        count_7 += 1
                        
                # Since 7 is prime, the intersection of any two distinct Sylow 7-subgroups is trivial.
                # Thus, each Sylow 7-subgroup contains exactly 6 elements of order 7.
                n_7 = count_7 // 6
                neg_q = (n_7 != 8)
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is 168",
    "¬Q: The number of Sylow 7-subgroups of G is not exactly 8"
]

N_HYP = 1
NEG_Q_INDEX = 1
