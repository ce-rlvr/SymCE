import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
        G, N = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(G.is_cyclic)
    except Exception:
        h1 = False
        
    try:
        Q = False
        if hasattr(N, 'is_subgroup') and N.is_subgroup(G):
            if hasattr(N, 'is_normal') and N.is_normal(G):
                order_G = G.order() if callable(getattr(G, 'order', None)) else G.order
                order_N = N.order() if callable(getattr(N, 'order', None)) else N.order
                quotient_order = order_G // order_N
                
                is_cyclic_quotient = False
                elements = G.elements if hasattr(G, 'elements') else list(G.generate())
                for g in elements:
                    k = 1
                    curr = g
                    while not N.contains(curr):
                        curr = curr * g
                        k += 1
                    if k == quotient_order:
                        is_cyclic_quotient = True
                        break
                Q = is_cyclic_quotient
            else:
                Q = False
        else:
            Q = False
    except Exception:
        Q = False
        
    neg_Q = not Q
    
    return [h1, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: The quotient group G/N is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1