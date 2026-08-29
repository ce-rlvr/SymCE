import math
from sympy.ntheory import jacobi_symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n is not a perfect square",
    "¬Q: sum_{a=1}^n (a|n) != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        n = int(witness)
        if not isinstance(witness, str) and n != witness:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: n is not a perfect square
    try:
        if n < 0:
            h1_ok = True
        else:
            root = math.isqrt(n)
            h1_ok = bool(root * root != n)
    except Exception:
        h1_ok = False

    # ¬Q: sum_{a=1}^n (a|n) != 0
    try:
        try:
            s = sum(jacobi_symbol(a, n) for a in range(1, n + 1))
            neg_q_ok = bool(s != 0)
        except ValueError:
            # If jacobi_symbol raises ValueError (e.g., for even n or negative n),
            # the expression is undefined, so the conclusion "sum == 0" fails.
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]