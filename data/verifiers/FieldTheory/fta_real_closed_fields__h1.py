import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, QQ, RR, CC, ZZ, I, Symbol, GF

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

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: i is a root of the polynomial x^2 + 1",
    "¬Q: The field extension R(i) is not an algebraically closed field"
]

def conditions(witness):
    try:
        # The witness must be a valid field R.
        is_field = getattr(witness, 'is_Field', False)
        # i is a root of x^2 + 1 (this is true by definition for the imaginary unit I)
        h1 = is_field and (I**2 + 1 == 0)
    except Exception:
        h1 = False

    try:
        if not getattr(witness, 'is_Field', False):
            neg_q = False
        # If R is the Real or Complex field, R(i) is the Complex field, which IS algebraically closed.
        elif witness == CC or witness == RR:
            neg_q = False
        elif hasattr(witness, 'name') and ('CC' in witness.name or 'Complex' in witness.name or 'RR' in witness.name or 'Real' in witness.name):
            neg_q = False
        else:
            # For other fields like QQ or finite fields, R(i) is NOT algebraically closed.
            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]