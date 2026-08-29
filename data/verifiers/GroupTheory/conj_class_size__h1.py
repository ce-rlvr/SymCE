import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def get_elements(G):
    if isinstance(G, (list, set, tuple)):
        return list(G)
    if hasattr(G, 'elements'):
        return list(G.elements)
    if hasattr(G, 'generate'):
        return list(G.generate())
    return list(G)

def conditions(witness) -> list[bool]:
    try:
        G, x = witness
    except Exception:
        return [False, False]
    
    try:
        elements = get_elements(G)
        h1_ok = x in elements
    except Exception:
        h1_ok = False
        
    try:
        elements = get_elements(G)
        conj_class = []
        for g in elements:
            c = g * x * g**-1
            if c not in conj_class:
                conj_class.append(c)
                
        centralizer = []
        for g in elements:
            if g * x == x * g:
                centralizer.append(g)
                
        neg_q_ok = (len(conj_class) * len(centralizer) != len(elements))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "¬Q: The size of the conjugacy class of x is not equal to the index of C_G(x) in G"
]

N_HYP = 1
NEG_Q_INDEX = 1