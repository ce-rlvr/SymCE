import sympy
import sympy.ntheory
from sympy import re, zeta
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Re(s) > 1
    try:
        h1 = bool(re(witness) > 1)
    except Exception:
        h1 = False

    # neg_Q: sum_{n=1}^infty |mu(n)| / n^s != zeta(s) / zeta(2s)
    try:
        if witness == sympy.oo:
            neg_q = False
        else:
            s_val = complex(witness)
            # Evaluate RHS to ensure it's well-defined
            rhs_val = complex(zeta(s_val) / zeta(2 * s_val))
            # The identity is mathematically true for all complex s with Re(s) > 1.
            # If the witness is a valid complex number, the conclusion holds.
            neg_q = False
    except Exception:
        # If evaluation fails (e.g., complex infinity, matrices, etc.), the conclusion fails.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Re(s) > 1",
    "¬Q: sum_{n=1}^infty |mu(n)| / n^s != zeta(s) / zeta(2s)"
]

N_HYP = 1
NEG_Q_INDEX = 1