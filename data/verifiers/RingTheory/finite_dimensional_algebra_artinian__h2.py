import sympy
from sympy import QQ, RR, CC, ZZ

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: A is finite-dimensional as a vector space over k",
    "¬Q: A is not an Artinian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1 = False
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('k_is_field', witness.get('is_field', False)))
        elif hasattr(witness, 'k_is_field'):
            val = witness.k_is_field
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_field'):
            val = witness.is_field
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'k') and hasattr(witness.k, 'is_Field'):
            h1 = bool(witness.k.is_Field)
        elif isinstance(witness, tuple) and len(witness) >= 1 and hasattr(witness[0], 'is_Field'):
            h1 = bool(witness[0].is_Field)
    except Exception:
        pass

    h2 = False
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('A_is_finite_dimensional', witness.get('is_finite_dimensional', False)))
        elif hasattr(witness, 'A_is_finite_dimensional'):
            val = witness.A_is_finite_dimensional
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_finite_dimensional'):
            val = witness.is_finite_dimensional
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'A') and hasattr(witness.A, 'is_finite_dimensional'):
            val = witness.A.is_finite_dimensional
            h2 = bool(val() if callable(val) else val)
        elif isinstance(witness, tuple) and len(witness) >= 2 and hasattr(witness[1], 'is_finite_dimensional'):
            val = witness[1].is_finite_dimensional
            h2 = bool(val() if callable(val) else val)
    except Exception:
        pass

    neg_q = False
    try:
        q = True
        if isinstance(witness, dict):
            q = bool(witness.get('A_is_artinian', witness.get('is_artinian', True)))
        elif hasattr(witness, 'A_is_artinian'):
            val = witness.A_is_artinian
            q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_artinian'):
            val = witness.is_artinian
            q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_Artinian'):
            val = witness.is_Artinian
            q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'A') and hasattr(witness.A, 'is_artinian'):
            val = witness.A.is_artinian
            q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'A') and hasattr(witness.A, 'is_Artinian'):
            val = witness.A.is_Artinian
            q = bool(val() if callable(val) else val)
        elif isinstance(witness, tuple) and len(witness) >= 2:
            if hasattr(witness[1], 'is_artinian'):
                val = witness[1].is_artinian
                q = bool(val() if callable(val) else val)
            elif hasattr(witness[1], 'is_Artinian'):
                val = witness[1].is_Artinian
                q = bool(val() if callable(val) else val)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]