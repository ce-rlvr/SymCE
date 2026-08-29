import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

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

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and (x in G) and (y in G)
    except Exception:
        h1 = False
        
    try:
        h2 = (math.gcd(x.order(), y.order()) == 1)
    except Exception:
        h2 = False
        
    try:
        elements = list(G.generate())
        xy = x * y
        
        C_G_x = set(g for g in elements if g * x == x * g)
        C_G_y = set(g for g in elements if g * y == y * g)
        C_G_xy = set(g for g in elements if g * xy == xy * g)
        
        intersection = C_G_x.intersection(C_G_y)
        
        cond1 = (C_G_xy == intersection)
        
        cl_xy = set(g * xy * (~g) for g in elements)
        size_cl_xy = len(cl_xy)
        
        cond2 = (size_cl_xy * len(intersection) == len(elements))
        
        neg_q = not (cond1 and cond2)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group, x and y are elements of G",
    "H_2: The orders of x and y are relatively prime",
    "not Q: C_G(xy) != C_G(x) intersection C_G(y) or size of Cl_G(xy) != index of intersection"
]

N_HYP = 2
NEG_Q_INDEX = 2