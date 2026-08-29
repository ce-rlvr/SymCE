import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, x, y, n = witness
    except Exception:
        return [False, False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = x in G
    except Exception:
        h2 = False
        
    try:
        h3 = y in G
    except Exception:
        h3 = False
        
    try:
        h4 = isinstance(n, (int, sympy.Integer))
    except Exception:
        h4 = False
        
    try:
        xy = x * y
        lhs = xy ** n
        
        # Commutator [y, x] = y^-1 x^-1 y x
        comm = (y ** -1) * (x ** -1) * y * x
        power = (n * (n - 1)) // 2
        rhs = (x ** n) * (y ** n) * (comm ** power)
        
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "H_3: y is an element of G",
    "H_4: n is an integer",
    "¬Q: identity does not hold"
]

N_HYP = 4
NEG_Q_INDEX = 4