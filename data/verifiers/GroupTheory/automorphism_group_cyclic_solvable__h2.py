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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    G, A = None, None
    if isinstance(witness, (tuple, list)) and len(witness) == 2:
        G, A = witness
    elif isinstance(witness, dict):
        G = witness.get('G')
        A = witness.get('A')
    else:
        G = getattr(witness, 'G', None)
        A = getattr(witness, 'A', None)

    try:
        h1 = False
        if G is not None and hasattr(G, 'is_cyclic'):
            h1 = bool(G.is_cyclic)
    except Exception:
        h1 = False

    try:
        neg_q = False
        if A is not None and hasattr(A, 'is_solvable'):
            neg_q = not bool(A.is_solvable)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "¬Q: A is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1