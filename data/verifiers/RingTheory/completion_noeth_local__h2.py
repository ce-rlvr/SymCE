import sympy
from sympy import ZZ, QQ
import sympy.abc

# Top-level setup for potential witness expressions
Z = ZZ
Q = QQ

def get_prop(w, prop, default=False):
    """Helper to safely extract properties from a dictionary or object."""
    try:
        if isinstance(w, dict):
            if prop in w:
                val = w[prop]
                return val() if callable(val) else val
            return default
        if hasattr(w, prop):
            val = getattr(w, prop)
            return val() if callable(val) else val
    except Exception:
        pass
    return default

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    
    Remaining hypotheses:
      H_1: R is a Noetherian local ring with maximal ideal m.
      
    Conclusion to negate:
      Q: \hat{R} is a Noetherian local ring.
    """
    try:
        # H_1: R is a Noetherian local ring
        is_noeth = get_prop(witness, 'is_noetherian', False)
        is_loc = get_prop(witness, 'is_local', False)
        h1 = bool(is_noeth and is_loc)
    except Exception:
        h1 = False

    try:
        # Q: \hat{R} is a Noetherian local ring
        # We check if the completion is both Noetherian and local.
        if isinstance(witness, dict) and 'completion_is_noetherian' in witness:
            q_noeth = get_prop(witness, 'completion_is_noetherian', True)
            q_local = get_prop(witness, 'completion_is_local', True)
            q = q_noeth and q_local
        elif hasattr(witness, 'completion_is_noetherian'):
            q_noeth = get_prop(witness, 'completion_is_noetherian', True)
            q_local = get_prop(witness, 'completion_is_local', True)
            q = q_noeth and q_local
        elif hasattr(witness, 'completion') or (isinstance(witness, dict) and 'completion' in witness):
            comp = get_prop(witness, 'completion')
            q_noeth = get_prop(comp, 'is_noetherian', True)
            q_local = get_prop(comp, 'is_local', True)
            q = q_noeth and q_local
        else:
            # If completion properties are not provided, we cannot verify the conclusion fails.
            # Assume Q holds, so neg_Q will be False.
            q = True
            
        neg_q = not bool(q)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    r"H_1: R is a Noetherian local ring with maximal ideal m",
    r"¬Q: \hat{R} is not a Noetherian local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1