import sympy
from sympy import symbols, Rational, Integer
import math
import itertools
import functools

# Top-level setup
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal in R",
    "¬Q: The ideal I does not have a primary decomposition in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1 = False
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative_ring', False))
        elif hasattr(witness, 'is_commutative_ring'):
            val = witness.is_commutative_ring
            h1 = bool(val() if callable(val) else val)
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            else:
                val = getattr(R, 'is_commutative_ring', False)
                h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    h2 = False
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('is_ideal', False))
        elif hasattr(witness, 'is_ideal'):
            val = witness.is_ideal
            h2 = bool(val() if callable(val) else val)
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if type(I).__name__ == 'Ideal' or 'Ideal' in str(type(I)):
                h2 = True
            else:
                val = getattr(I, 'is_ideal', False)
                h2 = bool(val() if callable(val) else val)
    except Exception:
        h2 = False

    neg_q = False
    try:
        if isinstance(witness, dict):
            has_pd = bool(witness.get('has_primary_decomposition', True))
            neg_q = not has_pd
        elif hasattr(witness, 'has_primary_decomposition'):
            val = witness.has_primary_decomposition
            has_pd = bool(val() if callable(val) else val)
            neg_q = not has_pd
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if hasattr(I, 'has_primary_decomposition'):
                val = I.has_primary_decomposition
                has_pd = bool(val() if callable(val) else val)
                neg_q = not has_pd
            elif hasattr(R, 'has_primary_decomposition'):
                val = R.has_primary_decomposition
                has_pd = bool(val() if callable(val) else val)
                neg_q = not has_pd
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]