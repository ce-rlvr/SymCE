import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "¬Q: The size of the conjugacy class of x is strictly greater than the order of the derived subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        G, x = witness
    except Exception:
        return [False, False]
        
    try:
        h1_ok = bool(x in G.elements)
    except Exception:
        h1_ok = False
        
    try:
        elements = list(G.elements)
        conj_class = set(~g * x * g for g in elements)
        c_size = len(conj_class)
        
        d_order = G.derived_subgroup().order()
        
        neg_q_ok = bool(c_size > d_order)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]