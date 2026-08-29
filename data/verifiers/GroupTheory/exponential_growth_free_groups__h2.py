import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    k = -1

    try:
        if isinstance(witness, (int, sympy.Integer)):
            k = int(witness)
            h1 = (k >= 0)
            h2 = (k >= 0)
        elif type(witness).__name__ == 'FreeGroup':
            k = len(witness.generators)
            h1 = True
            h2 = True
        elif isinstance(witness, tuple) and len(witness) == 2 and type(witness[0]).__name__ == 'FreeGroup':
            F, S = witness
            k = len(F.generators)
            h1 = True
            h2 = True
        elif hasattr(witness, 'generators') and hasattr(witness, 'rank'):
            k = int(witness.rank)
            h1 = True
            h2 = True
    except Exception:
        pass

    try:
        if h1 and h2:
            neg_q = (k < 2)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group of finite rank k",
    "H_2: S is a finite free generating set for F",
    "¬Q: The word growth function of F with respect to S is not strictly exponential"
]

N_HYP = 2
NEG_Q_INDEX = 2