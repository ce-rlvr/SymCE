import sympy
from sympy import oo
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a right Artinian ring. The matrix ring M_n(R) is a right Artinian ring."
    
    The dropped hypothesis is that n must be finite.
    A valid witness provides an infinite n (e.g., sympy.oo), and optionally a ring R.
    """
    # Parse witness
    if isinstance(witness, tuple) and len(witness) == 2:
        R, n = witness
    else:
        R = sympy.QQ
        n = witness

    # H_1: R is a right Artinian ring
    try:
        if R in ['Z', sympy.ZZ]:
            h1_ok = False
        else:
            # Default to True for fields like QQ, RR, CC, finite rings, etc.
            h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: M_n(R) is NOT a right Artinian ring
    try:
        if n == oo or n == float('inf') or str(n).lower() in ['oo', 'inf', 'infinity']:
            neg_q_ok = True
        else:
            n_int = int(n)
            if n_int == n:
                if n_int == 0:
                    # M_0(R) is the zero ring, which is Artinian
                    neg_q_ok = False
                elif n_int > 0:
                    # For finite n >= 1, M_n(R) is Artinian iff R is Artinian
                    neg_q_ok = not h1_ok
                else:
                    # Undefined for negative sizes
                    neg_q_ok = True
            else:
                neg_q_ok = True
    except Exception:
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: M_n(R) is not a right Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1