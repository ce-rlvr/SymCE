import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'order'):
            if callable(witness.order):
                order = witness.order()
            else:
                order = witness.order
        else:
            order = len(witness)
        
        h1 = bool(sympy.ntheory.isprime(order))
    except Exception:
        h1 = False

    try:
        is_cyclic_group = False
        if isinstance(witness, sympy.combinatorics.PermutationGroup):
            is_cyclic_group = bool(witness.is_cyclic)
        elif hasattr(witness, 'is_group') and witness.is_group:
            if hasattr(witness, 'is_cyclic'):
                is_cyclic_group = bool(witness.is_cyclic)
        
        neg_q = not is_cyclic_group
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is a prime number p",
    "¬Q: G is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1