import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z

# Top-level setup
Q = QQ
Z = ZZ

def conditions(witness):
    try:
        is_field = getattr(witness, 'is_Field', False)
    except Exception:
        is_field = False

    try:
        is_finite = False
        if is_field:
            if hasattr(witness, 'order') and witness.order < sympy.oo:
                is_finite = True
            elif witness.__class__.__name__ in ['FiniteField', 'GaloisField']:
                is_finite = True
            elif getattr(witness, 'is_finite', False):
                is_finite = True
    except Exception:
        is_finite = False

    # H_1: F is an infinite field
    try:
        h1_ok = bool(is_field and not is_finite)
    except Exception:
        h1_ok = False

    # H_2: \overline{F} is the algebraic closure of F
    # This is a definitional hypothesis that holds for any valid field.
    try:
        h2_ok = bool(is_field)
    except Exception:
        h2_ok = False

    # ¬Q: The cardinality of \overline{F} is not equal to the cardinality of F
    # For an infinite field, |\overline{F}| = |F|.
    # For a finite field, |\overline{F}| = \aleph_0 != |F|.
    try:
        if not is_field:
            neg_q_ok = False
        else:
            neg_q_ok = bool(is_finite)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    r"H_1: F is an infinite field",
    r"H_2: \overline{F} is the algebraic closure of F",
    r"¬Q: The cardinality of \overline{F} is not equal to the cardinality of F"
]

N_HYP = 2
NEG_Q_INDEX = 2