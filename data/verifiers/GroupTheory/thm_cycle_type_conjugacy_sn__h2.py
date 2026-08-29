import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, Permutation, PermutationGroup
from sympy.matrices import eye, zeros
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False, False]
    
    try:
        n = G.degree
        h1 = isinstance(G, PermutationGroup) and G.order() == math.factorial(n) and n >= 1
    except Exception:
        h1 = False

    try:
        same_cycle_type = (x.cycle_structure == y.cycle_structure)
        
        conjugate = False
        for g in G.elements:
            if g * x * g**-1 == y:
                conjugate = True
                break
        
        neg_q = (conjugate != same_cycle_type)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the symmetric group S_n for some positive integer n",
    "¬Q: It is not the case that x and y are conjugate in G if and only if they have the same cycle type"
]

N_HYP = 1
NEG_Q_INDEX = 1