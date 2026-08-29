import sympy

# Top-level setup
Z = sympy.S.Integers
N = sympy.S.Naturals
Q = sympy.S.Rationals
R = sympy.S.Reals

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    """
    # Convert standard Python collections to sympy FiniteSet for uniform property checking
    try:
        if isinstance(witness, (list, tuple, set)):
            witness = sympy.FiniteSet(*witness)
    except Exception:
        pass

    # H1: S is non-empty
    h1 = False
    try:
        if hasattr(witness, 'is_empty'):
            h1 = not witness.is_empty
        else:
            h1 = len(witness) > 0
    except Exception:
        h1 = False

    # H2: S is bounded below
    h2 = False
    try:
        if hasattr(witness, 'is_bounded_below'):
            # Use explicit property if available
            h2 = witness.is_bounded_below() if callable(witness.is_bounded_below) else witness.is_bounded_below
        elif hasattr(witness, 'inf'):
            # For sympy Sets, it is bounded below if the infimum is not -oo
            inf = witness.inf
            h2 = (inf is not None) and (inf != -sympy.oo)
    except Exception:
        h2 = False

    # neg_Q: S does NOT have an infimum in the real numbers
    neg_q = False
    try:
        if hasattr(witness, 'inf'):
            inf = witness.inf
            if inf is None:
                neg_q = True
            else:
                # The infimum is not in the real numbers if is_real is explicitly False
                # (e.g., sympy.oo.is_real is False)
                neg_q = (inf.is_real is False)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is non-empty",
    "H_2: S is bounded below",
    "¬Q: S does not have an infimum in the real numbers"
]

N_HYP = 2
NEG_Q_INDEX = 2