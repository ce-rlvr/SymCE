import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should provide the ring R, the subset/ideal P, and the element x.
    Expected witness format: tuple (R, P, x) or dict {'R': R, 'P': P, 'x': x}.
    For simplicity, R can be an integer m >= 2 representing the ring Z/mZ.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, P, x = witness
        elif isinstance(witness, dict):
            R = witness['R']
            P = witness['P']
            x = witness['x']
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    h1 = False
    try:
        if isinstance(R, int) and R >= 2:
            h1 = True
        elif hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        elif hasattr(R, 'is_Ring'):
            h1 = True
    except Exception:
        pass

    # H_2: x is an element of R such that x^n = 0 for some positive integer n
    h2 = False
    try:
        if isinstance(R, int) and R >= 2:
            if isinstance(x, int):
                # In Z/RZ, if x is nilpotent, its nilpotency index is <= R
                h2 = (pow(x % R, R, R) == 0)
        else:
            curr = x
            for _ in range(100):
                if curr == 0:
                    h2 = True
                    break
                if hasattr(curr, 'is_zero') and curr.is_zero:
                    h2 = True
                    break
                if hasattr(R, 'zero') and curr == R.zero:
                    h2 = True
                    break
                curr = curr * x
    except Exception:
        pass

    # ¬Q: x is NOT an element of P
    neg_q = False
    try:
        if callable(P):
            neg_q = not P(x)
        elif hasattr(P, 'contains'):
            neg_q = not P.contains(x)
        elif isinstance(R, int) and R >= 2:
            if isinstance(P, int):
                neg_q = (x % R) != (P % R)
            else:
                neg_q = (x % R) not in [e % R for e in P]
        else:
            if isinstance(P, (list, set, tuple)):
                neg_q = x not in P
            else:
                neg_q = x != P
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: x is an element of R such that x^n = 0 for some positive integer n",
    "¬Q: x is not an element of P"
]

N_HYP = 2
NEG_Q_INDEX = 2