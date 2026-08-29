import sympy

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    witness is expected to be a dict or a tuple (R, I) representing a ring and an ideal,
    or a custom object with relevant properties.
    """
    # If witness is a dict, use it directly
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get("is_commutative_ring_with_identity", False))
            h2 = bool(witness.get("is_noetherian", False))
            neg_q = not bool(witness.get("quotient_is_noetherian", True))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # Otherwise, try to extract R and I
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            R = witness
            I = None
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        h1 = False
        if hasattr(R, 'is_commutative_ring_with_identity'):
            val = R.is_commutative_ring_with_identity
            h1 = bool(val() if callable(val) else val)
        else:
            is_comm = getattr(R, 'is_commutative', True)
            has_id = getattr(R, 'has_identity', True)
            if callable(is_comm): is_comm = is_comm()
            if callable(has_id): has_id = has_id()
            h1 = bool(is_comm and has_id)
    except Exception:
        h1 = False

    # H_2: R is a Noetherian ring
    try:
        h2 = False
        if hasattr(R, 'is_noetherian'):
            val = R.is_noetherian
            h2 = bool(val() if callable(val) else val)
        elif hasattr(R, 'is_Noetherian'):
            val = R.is_Noetherian
            h2 = bool(val() if callable(val) else val)
        else:
            if R in (sympy.ZZ, sympy.QQ) or getattr(R, 'is_Field', False):
                h2 = True
            elif hasattr(R, 'domain') and hasattr(R, 'symbols'):
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The quotient ring R/I is NOT a Noetherian ring
    try:
        neg_q = False
        if hasattr(witness, 'quotient_is_noetherian'):
            val = witness.quotient_is_noetherian
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(R, 'quotient_is_noetherian'):
            val = R.quotient_is_noetherian
            neg_q = not bool(val(I) if callable(val) else val)
        elif hasattr(I, 'is_noetherian_quotient'):
            val = I.is_noetherian_quotient
            neg_q = not bool(val() if callable(val) else val)
        else:
            if hasattr(witness, 'is_noetherian'):
                val = witness.is_noetherian
                neg_q = not bool(val() if callable(val) else val)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "¬Q: The quotient ring R/I is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2