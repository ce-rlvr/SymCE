import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

F2 = free_group('x, y')[0]

def conditions(witness) -> list[bool]:
    F = None
    n = None
    try:
        if isinstance(witness, dict):
            F = witness.get('F', None)
            n = witness.get('n', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            F, n = witness
        else:
            n = witness
    except Exception:
        pass

    try:
        if F is not None:
            h1 = bool(type(F).__name__ == 'FreeGroup' and len(F.generators) == 2)
        else:
            h1 = True
    except Exception:
        h1 = False

    try:
        if isinstance(n, (int, float)) or (hasattr(n, 'is_integer') and n.is_integer):
            if int(n) == n:
                if n >= 0:
                    neg_q = False
                else:
                    neg_q = True
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group of rank 2",
    "¬Q: F does not contain a subgroup isomorphic to the free group of rank n"
]

N_HYP = 1
NEG_Q_INDEX = 1