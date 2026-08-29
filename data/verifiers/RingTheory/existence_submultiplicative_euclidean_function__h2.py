import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y

# Top-level setup: named object bindings
# We provide standard rings and polynomial rings that can serve as witnesses.
ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)
QQ_x_y = QQ.poly_ring(x, y)
ZZ_x_y = ZZ.poly_ring(x, y)

def conditions(witness) -> list[bool]:
    # H_1: R is an integral domain
    try:
        # In SymPy, domains like ZZ, QQ, and their polynomial rings are integral domains.
        # We check if it's explicitly known to be a UFD, PID, or Field.
        h1 = (getattr(witness, 'is_UFD', None) is True) or \
             (getattr(witness, 'is_PID', None) is True) or \
             (getattr(witness, 'is_Field', None) is True)
    except Exception:
        h1 = False

    # ¬Q: R does not admit a Euclidean function d such that d(a) <= d(ab) for all non-zero a, b.
    # A domain admits such a function if and only if it is a Euclidean domain.
    # For the standard commutative rings representable in SymPy, being a Euclidean domain 
    # is equivalent to being a Principal Ideal Domain (PID).
    # Thus, the conclusion fails (¬Q is True) if the ring is explicitly NOT a PID.
    try:
        if not hasattr(witness, 'is_PID'):
            neg_q = False
        else:
            neg_q = (witness.is_PID is False)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R does not admit a submultiplicative Euclidean function (R is not a Euclidean domain)"
]

N_HYP = 1
NEG_Q_INDEX = 1