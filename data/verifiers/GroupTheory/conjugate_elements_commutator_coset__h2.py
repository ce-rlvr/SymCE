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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        G, x, y = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = hasattr(G, 'elements') and hasattr(G, 'derived_subgroup')
    except Exception:
        h1 = False
        
    try:
        if not h1:
            h2 = False
        else:
            elements = list(G.elements)
            if x not in elements or y not in elements:
                h2 = False
            else:
                h2 = any(g * x * ~g == y for g in elements)
    except Exception:
        h2 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            D = G.derived_subgroup()
            D_elements = list(D.elements)
            neg_q = (~x * y) not in D_elements
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x and y are conjugate in G",
    "¬Q: x and y do not belong to the same left coset of the commutator subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2