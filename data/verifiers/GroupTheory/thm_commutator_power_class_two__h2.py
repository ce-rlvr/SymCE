import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Integer

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, n, x, y = witness
    except Exception:
        return [False, False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(n, (int, Integer))
    except Exception:
        h2 = False
        
    try:
        h3 = x in G
    except Exception:
        h3 = False
        
    try:
        h4 = y in G
    except Exception:
        h4 = False
        
    try:
        def comm(a, b):
            return (~a) * (~b) * a * b
        
        lhs = comm(x**n, y)
        rhs = comm(x, y)**n
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: n is an integer",
    "H_3: x is an element of G",
    "H_4: y is an element of G",
    "¬Q: comm(x**n, y) != comm(x, y)**n"
]

N_HYP = 4
NEG_Q_INDEX = 4