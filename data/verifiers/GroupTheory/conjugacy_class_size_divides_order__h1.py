import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, x = witness
    except Exception:
        return [False, False]
        
    # H_1: x is an element of G
    try:
        h1 = x in G
    except Exception:
        h1 = False
        
    # neg_Q: cardinality of conjugacy class of x does not divide order of G
    try:
        if hasattr(G, 'order') and callable(G.order):
            order = G.order()
        elif hasattr(G, 'order'):
            order = G.order
        else:
            order = len(G)
            
        try:
            elements = list(G)
        except Exception:
            if hasattr(G, 'generate') and callable(G.generate):
                elements = list(G.generate())
            else:
                elements = list(G.elements)
            
        conj_class = set()
        for g in elements:
            try:
                inv_g = g**-1
            except Exception:
                inv_g = ~g
            conj_class.add(g * x * inv_g)
            
        c_size = len(conj_class)
        
        if c_size == 0:
            neg_q = False
        else:
            if order == sympy.oo:
                neg_q = True
            else:
                neg_q = (int(order) % int(c_size) != 0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "¬Q: The cardinality of the conjugacy class of x does not divide the order of G"
]

N_HYP = 1
NEG_Q_INDEX = 1