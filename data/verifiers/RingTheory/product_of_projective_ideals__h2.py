import sympy
from sympy import symbols
import math
import itertools
import functools
import z3

x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        if isinstance(witness, dict) and 'is_commutative_ring' in witness:
            h1 = bool(witness['is_commutative_ring'])
        elif hasattr(witness, 'is_commutative_ring'):
            val = witness.is_commutative_ring
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'R') and hasattr(witness.R, 'is_commutative'):
            val = witness.R.is_commutative
            h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    try:
        q = True
        if isinstance(witness, dict) and 'is_product_ideal_fg_projective' in witness:
            q = bool(witness['is_product_ideal_fg_projective'])
        elif hasattr(witness, 'is_product_ideal_fg_projective'):
            val = witness.is_product_ideal_fg_projective
            q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'IJ_is_projective'):
            val = witness.IJ_is_projective
            q = bool(val() if callable(val) else val)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The product ideal IJ is not a finitely generated projective ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1