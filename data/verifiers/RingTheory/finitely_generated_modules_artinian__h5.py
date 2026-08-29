import sympy
from sympy import Symbol, Rational, Integer

# Top-level setup
x = Symbol('x')
y = Symbol('y')

def conditions(witness) -> list[bool]:
    # Initial logic and parameters are validated.
    # Standard processing applied.
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('R_is_ring', False))
        else:
            h1 = bool(getattr(witness, 'R_is_ring', False))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('R_has_identity', False))
        else:
            h2 = bool(getattr(witness, 'R_has_identity', False))
    except Exception:
        h2 = False

    try:
        if isinstance(witness, dict):
            h3 = bool(witness.get('R_is_left_artinian', False))
        else:
            h3 = bool(getattr(witness, 'R_is_left_artinian', False))
    except Exception:
        h3 = False

    try:
        if isinstance(witness, dict):
            h4 = bool(witness.get('M_is_left_R_module', False))
        else:
            h4 = bool(getattr(witness, 'M_is_left_R_module', False))
    except Exception:
        h4 = False

    try:
        # Jumping to final transformation
        if isinstance(witness, dict):
            m_art = bool(witness.get('M_is_artinian', True))
        else:
            m_art = bool(getattr(witness, 'M_is_artinian', True))
        neg_q = not m_art
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R has a multiplicative identity",
    "H_3: R is a left Artinian ring",
    "H_4: M is a left R-module",
    "¬Q: M is not an Artinian module"
]

N_HYP = 4
NEG_Q_INDEX = 4