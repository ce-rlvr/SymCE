import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        if isinstance(witness, dict):
            n = witness.get('n')
            F = witness.get('F')
            S = witness.get('S')
        else:
            n, F, S = witness
    except Exception:
        return [False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n > 0
    except Exception:
        h1 = False

    # H_2: F is a free group of rank n
    try:
        is_free_group = type(F).__name__ == 'FreeGroup'
        if is_free_group:
            rank = getattr(F, 'rank', None)
            if rank is None:
                rank = len(getattr(F, 'generators', []))
            h2 = (rank == n)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The cardinality of S is strictly less than n
    try:
        neg_q = hasattr(S, '__len__') and len(S) < n
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: F is a free group of rank n",
    "¬Q: The cardinality of S is strictly less than n"
]

N_HYP = 2
NEG_Q_INDEX = 2