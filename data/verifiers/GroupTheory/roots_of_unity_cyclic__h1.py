import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    try:
        # H_1: Let U_n be the set of all complex numbers z such that z^n = 1
        # This is a definitional hypothesis, so we just verify the witness is a valid number.
        if isinstance(witness, (str, bool)):
            h1_ok = False
        else:
            complex(witness)
            h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # ¬Q: U_n does NOT form a cyclic group of order n under complex multiplication
        # The conclusion holds iff n is a strictly positive integer.
        # If n <= 0 or n is not an integer, the conclusion fails (neg_Q is True).
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            n = int(witness)
            neg_q_ok = (n <= 0)
        elif isinstance(witness, float) and witness.is_integer():
            n = int(witness)
            neg_q_ok = (n <= 0)
        elif isinstance(witness, sympy.Expr) and witness.is_integer is True:
            n = int(witness)
            neg_q_ok = (n <= 0)
        else:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let U_n be the set of all complex numbers z such that z^n = 1",
    "¬Q: U_n does not form a cyclic group of order n under complex multiplication"
]

N_HYP = 1
NEG_Q_INDEX = 1