import sympy
from sympy import oo

# Top-level setup
# The witness is expected to be a dictionary, a 3-tuple, or an object 
# providing the properties of the field extension:
# is_separable (bool), separable_degree, and degree.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            is_sep = bool(witness.get('is_separable', False))
            sep_deg = witness.get('separable_degree', 1)
            deg = witness.get('degree', 1)
        elif isinstance(witness, tuple) and len(witness) == 3:
            is_sep, sep_deg, deg = witness
            is_sep = bool(is_sep)
        else:
            is_sep = bool(witness.is_separable)
            sep_deg = witness.separable_degree
            deg = witness.degree
            
        # The conclusion is: L/K is separable iff [L:K]_s == [L:K]
        # We want the negation of the conclusion to be True.
        # So it must NOT be the case that (is_sep <==> (sep_deg == deg))
        # which means is_sep != (sep_deg == deg)
        neg_q = bool(is_sep != (sep_deg == deg))
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: It is not true that the extension is separable iff separable degree equals degree"
]

N_HYP = 0
NEG_Q_INDEX = 0