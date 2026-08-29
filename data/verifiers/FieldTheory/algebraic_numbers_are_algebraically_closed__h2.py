import sympy
from sympy import QQ, RR, CC, ZZ

# Top-level setup: named object bindings that the witness expression may reference.
# For FieldTheory, we provide standard SymPy domains.

def conditions(witness) -> list[bool]:
    try:
        # H_1: Let Q be the field of rational numbers.
        # This is a contextual hypothesis. We interpret it as requiring the witness A to be a valid field.
        h1_ok = bool(getattr(witness, 'is_Field', False))
    except Exception:
        h1_ok = False

    try:
        # ¬Q: A is NOT an algebraically closed field.
        # In SymPy, CC is the standard algebraically closed field. 
        # Fields like QQ, RR, and finite extensions are not algebraically closed.
        is_alg_closed = (witness == CC)
        neg_q_ok = not is_alg_closed
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let Q be the field of rational numbers (witness A is a field)",
    "¬Q: A is not an algebraically closed field"
]

N_HYP = 1
NEG_Q_INDEX = 1