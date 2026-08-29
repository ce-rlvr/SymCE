import sympy
from sympy import S, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

ZZ = S.Integers
QQ = S.Rationals
RR = S.Reals
CC = S.Complexes

def is_ring(R):
    """Check if the witness represents a mathematical ring."""
    try:
        if R in [S.Integers, S.Rationals, S.Reals, S.Complexes]:
            return True
        if hasattr(R, 'is_Ring') and R.is_Ring:
            return True
        if hasattr(R, 'is_Field') and R.is_Field:
            return True
        if hasattr(R, 'zero') and hasattr(R, 'one'):
            return True
        if R == S.Zero or R == 0:
            return True
    except Exception:
        pass
    return False

def is_zero_ring(R):
    """Check if the witness is the trivial (zero) ring."""
    try:
        if R in [S.Integers, S.Rationals, S.Reals, S.Complexes]:
            return False
        if hasattr(R, 'zero') and hasattr(R, 'one'):
            return R.zero == R.one
        if R == S.Zero or R == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # H_1: R is a non-zero ring
    try:
        h1 = bool(is_ring(witness) and not is_zero_ring(witness))
    except Exception:
        h1 = False

    # ¬Q: The formal power series ring R is right Artinian
    # Mathematically, R[[x]] is right Artinian if and only if R is the zero ring.
    try:
        neg_q = bool(is_ring(witness) and is_zero_ring(witness))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a non-zero ring",
    "neg_Q: The formal power series ring over R is right Artinian"
]

N_HYP = 1
NEG_Q_INDEX = 1