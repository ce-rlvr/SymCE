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
    h1 = False
    h2 = True
    neg_q = False
    
    try:
        if hasattr(witness, 'elements'):
            h1 = True
            elements = list(witness.elements)
            for x in elements:
                for y in elements:
                    comm_xy = (x**-1) * (y**-1) * x * y
                    comm_yx = (y**-1) * (x**-1) * y * x
                    if (comm_xy**-1) != comm_yx:
                        neg_q = True
                        break
                if neg_q:
                    break
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3 and hasattr(witness[0], 'elements'):
                G, x, y = witness
                h1 = True
                comm_xy = (x**-1) * (y**-1) * x * y
                comm_yx = (y**-1) * (x**-1) * y * x
                if (comm_xy**-1) != comm_yx:
                    neg_q = True
            elif len(witness) == 2:
                x, y = witness
                try:
                    _ = (x**-1) * (y**-1) * x * y
                    h1 = True
                except Exception:
                    h1 = False
                
                if h1:
                    comm_xy = (x**-1) * (y**-1) * x * y
                    comm_yx = (y**-1) * (x**-1) * y * x
                    if (comm_xy**-1) != comm_yx:
                        neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The commutator is defined as comm(x, y) = x^-1 y^-1 x y",
    "¬Q: The inverse of the commutator comm(x, y) is not equal to comm(y, x)"
]

N_HYP = 2
NEG_Q_INDEX = 2