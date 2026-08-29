import math
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        n, H = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = int(n) == n and n >= 2
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(H, PermutationGroup) and H.degree <= n
    except Exception:
        h2 = False
        
    try:
        is_A_n = (H.order() == math.factorial(n) // 2) and all(p.is_even for p in H.generators)
        neg_q = not is_A_n
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than or equal to 2",
    "H_2: H is a subgroup of the symmetric group S_n",
    "¬Q: H is not the alternating group A_n"
]

N_HYP = 2
NEG_Q_INDEX = 2