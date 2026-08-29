import sympy
from sympy.combinatorics import PermutationGroup
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
        if isinstance(witness, (tuple, list)):
            G = witness[0]
            c = witness[1] if len(witness) > 1 else 1
        else:
            G = witness
            c = 1
    except Exception:
        return [False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        neg_q = not (bool(G.is_abelian) and c == 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: G is not an abelian group or c != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1