import sympy
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

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    """
    # H_1: n is an odd integer
    try:
        if not isinstance(witness, (int, sympy.Integer)) or isinstance(witness, bool):
            h1 = False
        else:
            h1 = (witness % 2 != 0)
    except Exception:
        h1 = False

    # neg_Q: The canonical modular inverse of 2 modulo n is NOT exactly (n+1)/2
    try:
        if not isinstance(witness, (int, sympy.Integer)) or isinstance(witness, bool):
            neg_q = False
        else:
            n = int(witness)
            # The canonical modular inverse is typically defined modulo |n|
            # For n=1 or n=-1, abs(n)=1, and pow(2, -1, 1) returns 0
            inv = pow(2, -1, abs(n))
            expected = (n + 1) // 2
            
            # The conclusion fails if the canonical inverse does not equal the formula
            neg_q = (inv != expected)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an odd integer",
    "¬Q: 2^{-1} mod n is not exactly equal to (n+1)/2"
]

N_HYP = 1
NEG_Q_INDEX = 1