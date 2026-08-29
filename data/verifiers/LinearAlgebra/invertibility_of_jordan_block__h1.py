import sympy
from sympy import Matrix, eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (J, lam), checks if it is a counterexample to the false conjecture:
    "J is an invertible matrix if and only if λ ≠ 0."
    """
    try:
        # The witness must provide both the matrix J and the scalar λ
        J, lam = witness
    except Exception:
        return [False]
        
    try:
        # Check if J is invertible (determinant is non-zero)
        is_invertible = bool(J.det() != 0)
        
        # Check if λ is non-zero
        lam_nonzero = bool(lam != 0)
        
        # The conclusion is: is_invertible == lam_nonzero
        # The negated conclusion is that this equivalence fails
        neg_q = (is_invertible != lam_nonzero)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: It is not the case that J is invertible iff λ ≠ 0"
]

N_HYP = 0
NEG_Q_INDEX = 0