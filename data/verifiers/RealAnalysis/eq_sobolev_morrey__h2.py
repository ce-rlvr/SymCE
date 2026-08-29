import sympy
import math

# Top-level setup
# No specific named algebra objects are required for this RealAnalysis conjecture.

def get_bool_attr(witness, names, default=False):
    """Helper to extract boolean properties or evaluate boolean methods from the witness."""
    for name in names:
        if isinstance(witness, dict) and name in witness:
            val = witness[name]
            return bool(val() if callable(val) else val)
        if hasattr(witness, name):
            val = getattr(witness, name)
            return bool(val() if callable(val) else val)
    return default

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    # H_1: n >= 1 is an integer and p > n
    try:
        n = None
        p = None
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
        elif hasattr(witness, 'n') and hasattr(witness, 'p'):
            n = witness.n
            p = witness.p
        elif isinstance(witness, tuple) and len(witness) >= 2:
            n = witness[0]
            p = witness[1]

        if n is not None and p is not None:
            if int(n) == n and n >= 1 and p > n:
                h1 = True
    except Exception:
        pass

    # H_2: There exists M > 0 such that the Sobolev norm ||u||_{W^{1,p}} <= M for all u in F
    try:
        h2 = get_bool_attr(witness, ['is_bounded_in_W1p', 'bounded_in_W1p', 'H2', 'h2', 'is_bounded'])
        if not h2 and hasattr(witness, 'M'):
            if hasattr(witness, 'check_W1p_bound'):
                h2 = bool(witness.check_W1p_bound(witness.M))
            elif hasattr(witness, 'is_bounded'):
                h2 = bool(witness.is_bounded(witness.M))
    except Exception:
        pass

    # neg_Q: The family does NOT admit continuous representatives that form a uniformly equicontinuous family
    try:
        if get_bool_attr(witness, ['neg_Q', 'neg_q']):
            neg_q = True
        else:
            is_ue = get_bool_attr(witness, ['is_uniformly_equicontinuous', 'uniformly_equicontinuous', 'Q', 'q'], default=True)
            if hasattr(witness, 'check_uniformly_equicontinuous'):
                is_ue = bool(witness.check_uniformly_equicontinuous())
            neg_q = not is_ue
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer and p > n",
    "H_2: The family is bounded in W^{1,p}(R^n)",
    "¬Q: The family does not admit continuous representatives that form a uniformly equicontinuous family on R^n"
]

N_HYP = 2
NEG_Q_INDEX = 2