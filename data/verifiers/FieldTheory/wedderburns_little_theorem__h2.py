import sympy
from sympy import isprime

# Top-level setup: named object bindings that the witness expression may reference.
# We represent the finite ring Z/nZ simply by the integer n.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9

# We also provide a representation for matrix rings over Z/pZ
class MatrixRing:
    def __init__(self, n, p):
        self.n = n
        self.p = p

M2_Z2 = MatrixRing(2, 2)
M2_Z3 = MatrixRing(2, 3)

def conditions(witness) -> list[bool]:
    # H_1: R is a finite ring
    h1_ok = False
    try:
        if isinstance(witness, (int, sympy.Integer)):
            # An integer n > 1 represents the finite ring Z/nZ
            h1_ok = int(witness) > 1
        elif isinstance(witness, MatrixRing):
            # Matrix rings over finite fields are finite rings
            h1_ok = witness.n >= 1 and isprime(witness.p)
    except Exception:
        h1_ok = False

    # ¬Q: R is not a commutative field
    neg_q_ok = False
    try:
        if isinstance(witness, (int, sympy.Integer)):
            # Z/nZ is a commutative field iff n is prime.
            # Thus, it is NOT a commutative field iff n is composite.
            neg_q_ok = not isprime(int(witness))
        elif isinstance(witness, MatrixRing):
            # Matrix rings of size >= 2 are not commutative, hence not commutative fields.
            if witness.n >= 2:
                neg_q_ok = True
            else:
                neg_q_ok = not isprime(witness.p)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a finite ring",
    "¬Q: R is not a commutative field"
]

N_HYP = 1
NEG_Q_INDEX = 1