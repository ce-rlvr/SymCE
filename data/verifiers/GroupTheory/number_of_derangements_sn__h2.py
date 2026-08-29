import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = G.degree
            
        h1 = isinstance(n, (int, sympy.Integer)) and n >= 1
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, n = witness
        else:
            G = witness
            n = G.degree
            
        if hasattr(G, 'elements'):
            elements = G.elements
        else:
            elements = G
            
        derangements = 0
        for p in elements:
            # A derangement has no fixed points in the domain 0 to n-1
            if all(p(i) != i for i in range(n)):
                derangements += 1
                
        formula = 0
        for k in range(n + 1):
            formula += (math.factorial(n) // math.factorial(k)) * ((-1)**k)
            
        neg_q = derangements != formula
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "¬Q: The number of derangements in the group does not equal n! sum_{k=0}^n (-1)^k / k!"
]

N_HYP = 1
NEG_Q_INDEX = 1