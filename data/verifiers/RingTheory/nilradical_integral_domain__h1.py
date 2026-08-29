import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer
from sympy.ntheory import isprime, factorint

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
    # We interpret an integer witness n as the ring Z/nZ (with n=0 representing Z).
    
    # H_1: R is an integral domain
    try:
        if isinstance(witness, int) or (hasattr(witness, 'is_integer') and witness.is_integer):
            n = abs(int(witness))
            if n == 0:
                h1 = True
            elif n == 1:
                h1 = False
            else:
                h1 = isprime(n)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: The nilradical of R is not the zero ideal
    try:
        if isinstance(witness, int) or (hasattr(witness, 'is_integer') and witness.is_integer):
            n = abs(int(witness))
            if n == 0:
                # Z has zero nilradical
                neg_q = False
            elif n == 1:
                # Z/1Z has zero nilradical
                neg_q = False
            else:
                # The nilradical of Z/nZ is zero iff n is square-free
                factors = factorint(n)
                is_sq_free = all(v == 1 for v in factors.values())
                neg_q = not is_sq_free
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The nilradical of R is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1