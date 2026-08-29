import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x, y, and z are elements of G",
    "¬Q: Commutator is not bilinear (conclusion fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False]
        G, x, y, z = witness
    except Exception:
        return [False, False, False]
        
    try:
        if isinstance(G, PermutationGroup):
            h1 = True
        else:
            h1 = hasattr(G, '__contains__')
    except Exception:
        h1 = False
        
    try:
        h2 = (x in G) and (y in G) and (z in G)
    except Exception:
        h2 = False
        
    try:
        # Standard group theory commutator: [a, b] = a^-1 b^-1 a b
        def comm(a, b):
            return (a**-1) * (b**-1) * a * b
            
        eq1 = comm(x * y, z) == comm(x, z) * comm(y, z)
        eq2 = comm(x, y * z) == comm(x, y) * comm(x, z)
        
        # The negated conclusion is True when bilinearity FAILS
        neg_q = not (eq1 and eq2)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]