import sympy
from sympy.combinatorics import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math
import itertools
import functools

class InfiniteCyclicGroup:
    @property
    def is_cyclic(self):
        return True
    
    def order(self):
        return sympy.oo

Z = InfiniteCyclicGroup()

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
    # H_1: G is a cyclic group
    try:
        h1 = False
        if witness == sympy.S.Integers or isinstance(witness, InfiniteCyclicGroup):
            h1 = True
        elif hasattr(witness, 'is_cyclic'):
            val = witness.is_cyclic
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'generators'):
            h1 = (len(witness.generators) == 1)
    except Exception:
        h1 = False

    # H_2: The order of G is n
    try:
        n = None
        if witness == sympy.S.Integers or isinstance(witness, InfiniteCyclicGroup):
            n = sympy.oo
        elif hasattr(witness, 'order'):
            val = witness.order
            n = val() if callable(val) else val
        
        h2 = (n is not None)
    except Exception:
        h2 = False

    # ¬Q: Aut(G) is not isomorphic to U(n)
    try:
        neg_q = False
        if h2:
            if n == sympy.oo:
                # U(oo) is undefined, so Aut(G) cannot be isomorphic to it
                neg_q = True
            elif isinstance(n, (int, sympy.Integer)) and n > 0:
                # For any finite cyclic group, Aut(G) is isomorphic to U(n)
                neg_q = False
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "H_2: The order of G is n",
    "¬Q: Aut(G) is not isomorphic to U(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2