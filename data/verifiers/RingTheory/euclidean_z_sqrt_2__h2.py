import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

def get_ab(w):
    if isinstance(w, tuple) and len(w) == 2:
        a, b = w
        if isinstance(a, int) and isinstance(b, int):
            return a, b
    try:
        expr = sympy.sympify(w).expand()
        a = expr.subs(sympy.sqrt(2), 0)
        b = sympy.expand((expr - a) / sympy.sqrt(2))
        if a.is_integer and b.is_integer:
            return int(a), int(b)
    except Exception:
        pass
    return None

def conditions(witness):
    try:
        ab = get_ab(witness)
        h1 = ab is not None
    except Exception:
        h1 = False

    try:
        if h1:
            a, b = ab
            neg_q = (a**2 - 2 * b**2 < 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: witness is an element of Z adjoined with sqrt(2)",
    "¬Q: N(witness) < 0, so N is not a Euclidean function"
]

N_HYP = 1
NEG_Q_INDEX = 1