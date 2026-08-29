import sympy
from sympy import eye, zeros, Rational, Integer, Matrix, Symbol
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    # Extract the element if the witness is provided as a tuple (e.g., (element, ring))
    if isinstance(witness, tuple) and len(witness) > 0:
        u = witness[0]
    else:
        u = witness

    # H_1: u is a unit in R
    try:
        if hasattr(u, 'is_Matrix') and u.is_Matrix:
            if u.is_square:
                # If all elements are integers, it's a unit in M_n(Z) iff determinant is 1 or -1
                if all(getattr(x, 'is_integer', False) or isinstance(x, int) for x in u):
                    h1 = abs(u.det()) == 1
                else:
                    # Otherwise, assume it's over a field where non-zero determinant implies invertibility
                    h1 = u.det() != 0
            else:
                h1 = False
        elif isinstance(u, int) or getattr(u, 'is_integer', False):
            # In the ring of integers, only 1 and -1 are units
            h1 = u in [1, -1]
        elif isinstance(u, (float, complex)) or getattr(u, 'is_rational', False) or getattr(u, 'is_real', False):
            # In fields (Rationals, Reals, Complex), any non-zero element is a unit
            h1 = u != 0
        else:
            # Fallback for other symbolic expressions
            h1 = u != 0
    except Exception:
        h1 = False

    # ¬Q: u is not equal to the multiplicative identity 1
    try:
        if hasattr(u, 'is_Matrix') and u.is_Matrix:
            neg_q = u != eye(u.shape[0])
        else:
            neg_q = u != 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: u is a unit in R",
    "¬Q: u is not equal to the multiplicative identity 1"
]

N_HYP = 1
NEG_Q_INDEX = 1