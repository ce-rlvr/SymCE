import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    """
    # H_1: R is a unique factorization domain
    try:
        if hasattr(witness, 'is_UFD'):
            h1 = bool(witness.is_UFD)
        elif hasattr(witness, 'is_ufd'):
            h1 = bool(witness.is_ufd)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: R is not integrally closed in K
    try:
        if hasattr(witness, 'is_integrally_closed'):
            is_int_closed = bool(witness.is_integrally_closed)
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            is_int_closed = True
        elif h1:
            # Mathematically, every UFD is integrally closed.
            is_int_closed = True
        else:
            # If we cannot determine integral closure, we fail safely.
            raise NotImplementedError
            
        neg_q = not is_int_closed
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: R is not integrally closed in K"
]

N_HYP = 1
NEG_Q_INDEX = 1