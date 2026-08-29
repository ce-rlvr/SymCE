import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics.permutations import Permutation
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
    if isinstance(witness, dict):
        A = witness.get('A')
        B = witness.get('B')
        G = witness.get('G')
    elif isinstance(witness, (tuple, list)) and len(witness) == 3:
        non_abelian = [x for x in witness if hasattr(x, 'is_abelian') and not x.is_abelian]
        if len(non_abelian) == 1:
            G = non_abelian[0]
            rem = list(witness)
            rem.remove(G)
            A, B = rem[0], rem[1]
        else:
            A, B, G = witness
    else:
        A, B, G = None, None, None

    try:
        h1 = bool(A.is_abelian) and A.order() >= 1 and A.order() != sympy.oo
    except Exception:
        h1 = False

    try:
        h2 = bool(B.is_abelian) and B.order() >= 1 and B.order() != sympy.oo
    except Exception:
        h2 = False

    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a finite abelian group",
    "H_2: B is a finite abelian group",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2