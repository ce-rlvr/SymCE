import sympy
import sympy.abc
from sympy import Rational, Integer

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Since SymPy does not have a native GradedRing class, the witness is expected to be 
    a dictionary or an object with boolean attributes representing the mathematical properties.
    """
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('I_is_homogeneous', False))
        else:
            h1 = bool(getattr(witness, 'I_is_homogeneous', False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            q = bool(witness.get('quotient_has_natural_grading', True))
        else:
            q = bool(getattr(witness, 'quotient_has_natural_grading', True))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a homogeneous ideal of R",
    "¬Q: The quotient ring R/I does not have a natural grading such that the canonical projection from R to R/I is a graded ring homomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1