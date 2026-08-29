import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def conditions(witness) -> list[bool]:
    try:
        G, x = witness
    except Exception:
        return [False, False]
        
    try:
        if hasattr(G, 'contains'):
            h1_ok = bool(G.contains(x))
        else:
            h1_ok = bool(x in G)
    except Exception:
        h1_ok = False

    try:
        if hasattr(G, 'generate_elements'):
            elements = list(G.generate_elements())
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        C_G_x = [y for y in elements if x * y == y * x]
        index = len(elements) / len(C_G_x)
            
        K = set()
        for y in elements:
            comm = (x**-1) * (y**-1) * x * y
            K.add(comm)
            
        neg_q_ok = (len(K) != index)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "¬Q: The cardinality of the set of commutators is not exactly the index of the centralizer"
]

N_HYP = 1
NEG_Q_INDEX = 1