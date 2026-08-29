import sympy
from sympy.ntheory import factorint
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
    # Extract the field size q from the witness
    try:
        if hasattr(witness, 'order') and callable(witness.order):
            q = int(witness.order())
        elif hasattr(witness, 'order'):
            q = int(witness.order)
        elif hasattr(witness, 'mod'):
            q = int(witness.mod)
        else:
            q = int(witness)
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

    # ¬Q: The number of non-zero squares in F_q is NOT exactly (q-1)/2
    try:
        if h1_ok:
            p = list(factors.keys())[0]
            
            # In a finite field of characteristic 2, every element is a square.
            # Thus, there are q - 1 non-zero squares.
            # In a finite field of odd characteristic, exactly half of the 
            # non-zero elements are squares, giving (q - 1) / 2.
            if p == 2:
                actual_squares = q - 1
            else:
                actual_squares = (q - 1) // 2
            
            claimed_squares = (q - 1) / 2
            
            # The conclusion fails if the actual number of squares does not equal the claimed amount
            neg_q_ok = float(actual_squares) != float(claimed_squares)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "¬Q: The number of non-zero squares in F_q is not exactly (q-1)/2"
]

N_HYP = 1
NEG_Q_INDEX = 1