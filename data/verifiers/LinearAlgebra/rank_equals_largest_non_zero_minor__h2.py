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
    A = None
    r = None
    
    # Extract A and r from the witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            A, r = witness
        elif isinstance(witness, dict) and 'A' in witness and 'r' in witness:
            A = witness['A']
            r = witness['r']
            
        # H_1: A is a matrix and r is an integer
        h1 = hasattr(A, 'rank') and isinstance(r, (int, sympy.Integer))
    except Exception:
        h1 = False

    # ¬Q: The rank of A is not equal to r
    try:
        if h1:
            neg_q = bool(A.rank() != r)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a matrix and r is an integer",
    "¬Q: The rank of A is not equal to r"
]

N_HYP = 1
NEG_Q_INDEX = 1