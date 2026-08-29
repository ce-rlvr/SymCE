import sympy
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, H, N = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = bool(N.is_normal(G))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(H.is_subgroup(G))
    except Exception:
        h2 = False
        
    try:
        h3 = bool(N.is_subgroup(H))
    except Exception:
        h3 = False
        
    try:
        idx_GH = G.order() // H.order()
        idx_GNHN = (G.order() // N.order()) // (H.order() // N.order())
        neg_q = bool(idx_GH != idx_GNHN)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "H_3: N is a subgroup of H",
    "¬Q: The index of H in G is not equal to the index of H/N in G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3