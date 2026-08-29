import sympy
import sympy.ntheory
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
    if isinstance(witness, tuple) and len(witness) == 2:
        n, deg_K = witness
        check_deg = True
    else:
        n = witness
        check_deg = False

    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n >= 3
    except Exception:
        h1 = False

    try:
        if h1:
            actual_deg = sympy.ntheory.totient(int(n))
            if check_deg:
                h2 = bool(deg_K == actual_deg)
            else:
                h2 = True
                deg_K = actual_deg
        else:
            h2 = False
            deg_K = None
    except Exception:
        h2 = False
        deg_K = None

    try:
        if h1 and deg_K is not None:
            neg_q = not bool(deg_K == sympy.ntheory.totient(int(n)))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "H_2: K is the splitting field of Phi_n(x) over Q",
    "¬Q: The degree of K over Q is not equal to phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2