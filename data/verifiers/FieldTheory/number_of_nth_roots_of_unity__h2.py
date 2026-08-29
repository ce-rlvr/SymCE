import math
from sympy.ntheory import factorint
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
    Check if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (q, n) where q is the field size and n is the exponent.
    """
    try:
        if isinstance(witness, dict):
            q = int(witness['q'])
            n = int(witness['n'])
        elif isinstance(witness, (tuple, list)):
            q = int(witness[0])
            n = int(witness[1])
        else:
            # If only q is provided, we use n = 0 as it is the standard counterexample
            q = int(witness)
            n = 0
    except Exception:
        return [False, False]

    # H_1: F_q is a finite field with q elements
    # This is true if and only if q is a prime power (q >= 2)
    try:
        if q >= 2:
            factors = factorint(q)
            h1_ok = (len(factors) == 1)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: The number of elements x \in F_q satisfying x^n = 1 is NOT exactly \gcd(n, q-1)
    try:
        if q >= 2:
            # In F_q, the multiplicative group F_q^* is cyclic of order q-1.
            # The number of solutions to x^n = 1 in F_q^* is exactly gcd(n, q-1).
            # The element 0 satisfies 0^n = 1 if and only if n == 0 (since 0^0 = 1 in rings).
            actual_solutions = math.gcd(abs(n), abs(q - 1))
            if n == 0:
                actual_solutions += 1
            
            expected_solutions = math.gcd(abs(n), abs(q - 1))
            neg_q_ok = (actual_solutions != expected_solutions)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "¬Q: The number of elements x in F_q satisfying x^n = 1 is not exactly gcd(n, q-1)"
]

N_HYP = 1
NEG_Q_INDEX = 1