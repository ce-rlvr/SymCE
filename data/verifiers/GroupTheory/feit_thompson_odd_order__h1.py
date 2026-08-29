import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
        if hasattr(witness, 'order'):
            if callable(witness.order):
                o = witness.order()
            else:
                o = witness.order
        else:
            o = None
        
        h1 = isinstance(o, (int, sympy.Integer)) and (o % 2 == 1)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, PermutationGroup):
            q = bool(witness.is_solvable)
        elif hasattr(witness, 'is_solvable'):
            q = bool(witness.is_solvable)
        else:
            q = False
        neg_q = not q
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The order of G is an odd integer",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1