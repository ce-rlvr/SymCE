import math
import itertools
import functools
import sympy
from sympy import oo, nan
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
class InfiniteCyclicGroup:
    def __str__(self):
        return "Z"
    
    def order(self):
        return oo
        
    def is_normal(self, N):
        if isinstance(N, (InfiniteCyclicSubgroup, InfiniteCyclicGroup)):
            return True
        return False

class InfiniteCyclicSubgroup:
    def __init__(self, index):
        self.index = index
        
    def __str__(self):
        return f"{self.index}Z"
        
    def order(self):
        if self.index == 0:
            return 1
        return oo

Z = InfiniteCyclicGroup()

def nZ(n):
    return InfiniteCyclicSubgroup(n)

def quotient_group_order(G, N):
    if isinstance(G, InfiniteCyclicGroup):
        if isinstance(N, InfiniteCyclicSubgroup):
            if N.index == 0:
                return oo
            return abs(N.index)
        if isinstance(N, InfiniteCyclicGroup):
            return 1
    return G.order() / N.order()

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
        G, N = witness
    except Exception:
        return [False, False]
        
    # H_1: N is a normal subgroup of G
    try:
        h1 = bool(G.is_normal(N))
    except Exception:
        h1 = False
        
    # neg_Q: The order of G/N is not equal to |G| / |N|
    try:
        q_order = quotient_group_order(G, N)
        g_order = G.order()
        n_order = N.order()
        
        rhs = g_order / n_order
        
        # In sympy, oo / oo evaluates to nan.
        if rhs is nan or str(rhs) == 'nan':
            neg_q = True
        else:
            neg_q = bool(q_order != rhs)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The order of G/N is not equal to |G| / |N|"
]

N_HYP = 1
NEG_Q_INDEX = 1