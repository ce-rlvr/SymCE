import sympy
from sympy import totient
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
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to provide the integer n and the group U (which was dropped from hypotheses).
    """
    n, R, U = None, None, None
    if isinstance(witness, dict):
        n = witness.get('n')
        R = witness.get('R')
        U = witness.get('U')
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 2:
            n, U = witness
        elif len(witness) >= 3:
            n, R, U = witness[:3]
    else:
        n = witness

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # H_2: R is the ring of integers modulo n
    # Since R is uniquely determined by n, we consider this satisfied if n is valid.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # ¬Q: The order of the group U is not equal to \phi(n)
    try:
        if U is None:
            neg_q = False
        else:
            if hasattr(U, 'order'):
                if callable(U.order):
                    order_U = U.order()
                else:
                    order_U = U.order
            else:
                order_U = len(U)
            
            neg_q = bool(order_U != totient(n))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: R is the ring of integers modulo n",
    "¬Q: The order of the group U is not equal to phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2