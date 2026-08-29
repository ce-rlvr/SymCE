import sympy
from sympy.ntheory import legendre_symbol

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

def conditions(witness):
    try:
        p = int(witness)
        if p != witness:
            h1 = False
        else:
            h1 = p > 3
    except Exception:
        h1 = False

    try:
        p = int(witness)
        if p != witness:
            q = False
        elif not sympy.isprime(p):
            # The Legendre symbol is only defined for primes.
            # If p is composite, the conclusion statement is invalid/false.
            q = False
        else:
            val = legendre_symbol(3, p)
            q = (val == 1) == (p % 12 in (1, 11))
    except Exception:
        q = False

    return [h1, not q]

CONDITION_LABELS = [
    "H_1: p is strictly greater than 3",
    "¬Q: The Legendre symbol (3/p) does not equal 1 if and only if p is congruent to 1 or 11 modulo 12 (or is undefined)"
]

N_HYP = 1
NEG_Q_INDEX = 1