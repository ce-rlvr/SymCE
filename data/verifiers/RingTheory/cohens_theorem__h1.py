import sympy
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.abc import x, y, z
from sympy.polys.rings import PolyRing
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Every prime ideal of R is a finitely generated ideal
    try:
        if isinstance(witness, dict) and 'prime_ideals_finitely_generated' in witness:
            h1 = bool(witness['prime_ideals_finitely_generated'])
        elif hasattr(witness, 'prime_ideals_finitely_generated'):
            h1 = bool(witness.prime_ideals_finitely_generated)
        elif hasattr(witness, 'is_simple') and witness.is_simple:
            h1 = True
        elif isinstance(witness, PolyRing):
            h1 = True
        elif isinstance(witness, str):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: R is NOT a Noetherian ring
    try:
        if isinstance(witness, dict) and 'is_noetherian' in witness:
            neg_q = not bool(witness['is_noetherian'])
        elif hasattr(witness, 'is_noetherian'):
            neg_q = not bool(witness.is_noetherian)
        elif isinstance(witness, PolyRing):
            neg_q = False
        elif isinstance(witness, str):
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Every prime ideal of R is a finitely generated ideal",
    "¬Q: R is not a Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1