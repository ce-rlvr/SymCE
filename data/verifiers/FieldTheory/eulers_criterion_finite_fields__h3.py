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
    try:
        q, a = witness
    except Exception:
        return [False, False, False]

    # H1: F_q is a finite field with q elements
    try:
        q_int = int(q)
        if q_int < 2:
            h1 = False
            p = None
        else:
            factors = factorint(q_int)
            if len(factors) == 1:
                h1 = True
                p = list(factors.keys())[0]
            else:
                h1 = False
                p = None
    except Exception:
        h1 = False
        p = None

    # H2: The characteristic of F_q is an odd prime
    try:
        if h1 and p is not None and p % 2 != 0:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: a is a square in F_q iff a^((q-1)/2) == 1 is FALSE
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            is_zero = False
            if isinstance(a, (list, tuple)):
                if len(a) > 0 and all(c == 0 for c in a):
                    is_zero = True
            else:
                try:
                    if int(a) % p == 0:
                        is_zero = True
                except Exception:
                    pass
            
            if is_zero:
                # 0 is a square (0^2 = 0), but 0^((q-1)/2) = 0 != 1
                # Thus the equivalence fails for a = 0
                neg_q = True
            else:
                # For any non-zero element in F_q, Euler's criterion holds true
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: The characteristic of F_q is an odd prime",
    "¬Q: a is a square in F_q but a^((q-1)/2) != 1, or vice versa"
]

N_HYP = 2
NEG_Q_INDEX = 2