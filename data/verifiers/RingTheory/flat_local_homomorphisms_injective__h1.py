import sympy
from sympy import eye, zeros
import z3
import itertools
import functools
import math

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Verifies the counterexample to the conjecture "Flat Local Homomorphisms are Injective".
    Since no finite counterexample exists (any flat algebra over a finite local ring is 
    faithfully flat, hence injective), the witness must be an infinite ring construction 
    (e.g., an affine scheme coordinate ring) provided as a custom object or dictionary 
    implementing the required mathematical properties.
    """
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_local_homomorphism', False))
        else:
            h1 = bool(witness.is_local_homomorphism())
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('is_flat', False))
        else:
            h2 = bool(witness.is_flat())
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            neg_q = not bool(witness.get('is_injective', True))
        else:
            neg_q = not bool(witness.is_injective())
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: \\phi: R \\to S is a local ring homomorphism",
    "H_2: S is a flat R-module via the homomorphism \\phi",
    "¬Q: The homomorphism \\phi is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2