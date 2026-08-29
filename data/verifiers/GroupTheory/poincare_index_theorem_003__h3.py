import math
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, H, n = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False
        
    try:
        try:
            n_int = int(n)
            is_valid_n = (n == n_int) and (n_int >= 0)
        except Exception:
            is_valid_n = False
            
        if is_valid_n:
            fact_n = math.factorial(n_int)
            exists = False
            for K in G.normal_subgroups():
                if K.is_subgroup(H):
                    index = G.order() // K.order()
                    if fact_n % index == 0:
                        exists = True
                        break
            neg_q = not exists
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: G is a group", "H_2: H is a subgroup of G", "not Q: no normal subgroup K of G in H has index dividing n factorial"]

N_HYP = 2
NEG_Q_INDEX = 2