import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    Checks if the given witness satisfies the remaining hypotheses and falsifies the conclusion.
    Since SymPy does not natively support abstract ring completions and flatness,
    the witness is expected to be a dictionary or an object with boolean attributes.
    """
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_commutative", False)) and bool(witness.get("is_Noetherian", False))
        else:
            h1 = bool(getattr(witness, "is_commutative", False)) and bool(getattr(witness, "is_Noetherian", False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get("is_I_adic_completion", False))
        else:
            h2 = bool(getattr(witness, "is_I_adic_completion", False))
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            is_flat = bool(witness.get("is_flat", True))
        else:
            is_flat = bool(getattr(witness, "is_flat", True))
        neg_q = not is_flat
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: R_hat is the I-adic completion of R",
    "¬Q: R_hat is not a flat R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2