import sympy
from sympy.abc import x, y, z
from sympy import Rational, Integer
import math
import itertools
import functools

# Top-level setup for abstract witness objects
class AbstractRing:
    """
    A mock class to represent a ring with specific properties,
    since SymPy does not natively support graded rings and their R_0 subrings.
    """
    def __init__(self, is_noetherian=False, R_0_is_noetherian=False, is_fg_R_0_algebra=False):
        self.is_noetherian = bool(is_noetherian)
        self.R_0_is_noetherian = bool(R_0_is_noetherian)
        self.is_fg_R_0_algebra = bool(is_fg_R_0_algebra)

Ring = AbstractRing
GradedRing = AbstractRing

def conditions(witness) -> list[bool]:
    h1 = False
    q1 = True
    q2 = True
    
    try:
        if hasattr(witness, 'is_noetherian'):
            h1 = bool(witness.is_noetherian)
            q1 = bool(getattr(witness, 'R_0_is_noetherian', True))
            q2 = bool(getattr(witness, 'is_fg_R_0_algebra', getattr(witness, 'is_finitely_generated_R_0_algebra', True)))
        elif isinstance(witness, dict):
            h1 = bool(witness.get('is_noetherian', False))
            q1 = bool(witness.get('R_0_is_noetherian', True))
            q2 = bool(witness.get('is_fg_R_0_algebra', witness.get('is_finitely_generated_R_0_algebra', True)))
        elif isinstance(witness, (list, tuple)) and len(witness) >= 3:
            h1 = bool(witness[0])
            q1 = bool(witness[1])
            q2 = bool(witness[2])
    except Exception:
        pass

    # The conclusion is: R_0 is Noetherian AND R is a finitely generated R_0-algebra.
    # We want the negation of this conclusion.
    neg_q = not (q1 and q2)
    
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "¬Q: R_0 is not a Noetherian ring or R is not a finitely generated R_0-algebra"
]

N_HYP = 1
NEG_Q_INDEX = 1