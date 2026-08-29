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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            x = witness.get('x')
            y = witness.get('y')
            z = witness.get('z')
            n = witness.get('n')
            if F is None and hasattr(x, 'group'):
                F = x.group
        elif len(witness) == 5:
            F, x, y, z, n = witness
        elif len(witness) == 4:
            x, y, z, n = witness
            F = getattr(x, 'group', None)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False

    try:
        h2 = (getattr(x, 'group', None) == F) and (getattr(y, 'group', None) == F) and (x * y != y * x)
    except Exception:
        h2 = False

    try:
        h3 = (getattr(z, 'group', None) == F)
    except Exception:
        h3 = False

    try:
        neg_q = isinstance(n, (int, sympy.Integer)) and n not in (1, -1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: x, y in F such that x*y != y*x",
    "H_3: z in F",
    "¬Q: n != 1 and n != -1"
]

N_HYP = 3
NEG_Q_INDEX = 3