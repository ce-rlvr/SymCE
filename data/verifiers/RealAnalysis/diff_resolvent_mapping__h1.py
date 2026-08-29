import sympy as sp
from sympy import eye, zeros
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

def conditions(witness) -> list[bool]:
    # H_1: rho(A) is the resolvent set of A
    try:
        h1 = isinstance(witness, sp.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # H_2: R(lambda) is the resolvent mapping defined on rho(A)
    try:
        h2 = isinstance(witness, sp.MatrixBase) and witness.is_square
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails.
    # The conclusion states R maps to M_n(R) and R'(lambda) = R(lambda)^2.
    # The derivative identity R'(lambda) = R(lambda)^2 is algebraically always true.
    # The conclusion fails if and only if R(lambda) does not map to M_n(R),
    # which happens exactly when A has complex entries.
    try:
        if not (isinstance(witness, sp.MatrixBase) and witness.is_square):
            neg_q = False
        else:
            is_real = True
            for entry in witness:
                entry_sp = sp.sympify(entry)
                im_part = sp.im(entry_sp)
                if im_part.is_zero is False:
                    is_real = False
                    break
                elif im_part.is_zero is None:
                    if entry_sp.has(sp.I):
                        is_real = False
                        break
            neg_q = not is_real
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: rho(A) is the resolvent set of A",
    "H_2: R(lambda) is the resolvent mapping",
    "¬Q: R does not map to M_n(R) or R'(lambda) != R(lambda)^2"
]

N_HYP = 2
NEG_Q_INDEX = 2