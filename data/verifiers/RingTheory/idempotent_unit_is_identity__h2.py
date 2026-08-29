import sympy
from sympy import eye, zeros, Matrix
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: R is a ring with identity 1_R
    try:
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            h1_ok = bool(witness.rows == witness.cols)
            identity = eye(witness.rows)
        else:
            # Verify it supports ring-like operations (addition and multiplication)
            _ = witness * witness
            _ = witness + witness
            h1_ok = True
            identity = 1
    except Exception:
        h1_ok = False
        identity = None

    # H_2: u is an idempotent element, meaning u^2 = u
    try:
        h2_ok = bool(witness * witness == witness)
    except Exception:
        h2_ok = False

    # ¬Q: u != 1_R
    try:
        if identity is not None:
            neg_q_ok = bool(witness != identity)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a ring with identity 1_R",
    "H_2: u is an idempotent element (u^2 = u)",
    "¬Q: u != 1_R"
]

N_HYP = 2
NEG_Q_INDEX = 2