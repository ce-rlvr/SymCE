import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

try:
    from sympy.combinatorics import free_group
    F_free, a, b = free_group("a b")
except Exception:
    F_free = "FreeGroup"

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (F, n, x, y), check the remaining hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            n = witness.get('n')
            x = witness.get('x')
            y = witness.get('y')
        else:
            F, n, x, y = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a free group
    try:
        h1 = False
        if type(F).__name__ == 'FreeGroup':
            h1 = True
        elif F == "FreeGroup":
            h1 = True
        elif isinstance(F, str) and "FreeGroup" in F:
            h1 = True
        elif hasattr(F, 'is_FreeGroup') and F.is_FreeGroup:
            h1 = True
        elif F is sympy.S.Integers:
            h1 = True
    except Exception:
        h1 = False

    # H_2: n is a non-zero integer
    try:
        h2 = isinstance(n, int) and n != 0
    except Exception:
        h2 = False

    # H_3: x^n = y^n
    try:
        h3 = bool(x**n == y**n)
    except Exception:
        h3 = False

    # ¬Q: x != y
    try:
        neg_q = bool(x != y)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: n is a non-zero integer",
    "H_3: x^n = y^n",
    "¬Q: x != y"
]

N_HYP = 3
NEG_Q_INDEX = 3