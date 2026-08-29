import sympy
from sympy import symbols

x = symbols('x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_field_F', False))
        else:
            h1 = bool(getattr(witness, 'is_field_F', False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('is_algebraic_extension', False))
        else:
            h2 = bool(getattr(witness, 'is_algebraic_extension', False))
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            h3 = bool(witness.get('splits_completely', False))
        else:
            h3 = bool(getattr(witness, 'splits_completely', False))
    except Exception:
        h3 = False

    try:
        if isinstance(witness, dict):
            neg_q = not bool(witness.get('is_algebraically_closed_field_E', True))
        else:
            neg_q = not bool(getattr(witness, 'is_algebraically_closed_field_E', True))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an algebraic extension of F",
    "H_3: Every non-constant polynomial over F splits completely into linear factors over E",
    "¬Q: E is not an algebraically closed field"
]

N_HYP = 3
NEG_Q_INDEX = 3