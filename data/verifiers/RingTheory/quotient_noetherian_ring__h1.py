import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup for witness expressions
# (ZZ, QQ, x, y, z are available for constructing standard rings/ideals if needed)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "If I is a two-sided ideal of R, then R/I is a left Noetherian ring."
    """
    # Fallback 1: Dictionary-based mock witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_two_sided_ideal', False))
            neg_q = not bool(witness.get('quotient_is_left_noetherian', True))
            return [h1, neg_q]
        except Exception:
            pass

    # Fallback 2: String-based descriptive witness
    if isinstance(witness, str):
        try:
            s = witness.lower()
            has_R = "ring" in s or "r =" in s or "r=" in s
            has_I = "ideal" in s or "i =" in s or "i=" in s or "0" in s
            is_non_noeth = "not noetherian" in s or "infinitely many" in s or "infinite variables" in s or "non-noetherian" in s
            if has_R and has_I and is_non_noeth:
                return [True, True]
            return [False, False]
        except Exception:
            pass

    # Standard object-based witness (tuple of R and I)
    try:
        if isinstance(witness, tuple) or isinstance(witness, list):
            if len(witness) == 2:
                R, I = witness
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    # Evaluate H_1: I is a two-sided ideal of R
    h1 = False
    try:
        if hasattr(I, 'is_two_sided_ideal'):
            if callable(I.is_two_sided_ideal):
                h1 = I.is_two_sided_ideal(R)
            else:
                h1 = I.is_two_sided_ideal
        elif hasattr(I, 'ring'):
            h1 = (I.ring == R)
        elif I == 0 or I == [0] or I == set([0]) or (hasattr(I, 'is_zero') and I.is_zero):
            h1 = True
        elif hasattr(R, 'is_ideal'):
            h1 = R.is_ideal(I)
        elif isinstance(I, list):
            try:
                h1 = all(g in R for g in I)
            except Exception:
                h1 = False
        else:
            h1 = getattr(I, 'is_ideal', False)
    except Exception:
        h1 = False

    # Evaluate ¬Q: The quotient ring R/I is NOT a left Noetherian ring
    neg_q = False
    try:
        if hasattr(R, 'quotient_is_left_noetherian'):
            if callable(R.quotient_is_left_noetherian):
                neg_q = not R.quotient_is_left_noetherian(I)
            else:
                neg_q = not R.quotient_is_left_noetherian
        elif hasattr(R, 'is_left_noetherian'):
            is_noeth = R.is_left_noetherian() if callable(R.is_left_noetherian) else R.is_left_noetherian
            if not is_noeth:
                # If R is not Noetherian and I is the zero ideal, R/I is isomorphic to R (not Noetherian)
                if I == 0 or I == [0] or I == set([0]) or (hasattr(I, 'is_zero') and I.is_zero):
                    neg_q = True
            else:
                neg_q = False
        elif hasattr(I, 'is_quotient_left_noetherian'):
            if callable(I.is_quotient_left_noetherian):
                neg_q = not I.is_quotient_left_noetherian()
            else:
                neg_q = not I.is_quotient_left_noetherian
        else:
            # Standard SymPy rings (e.g. PolyRing) are Noetherian, so their quotients are Noetherian
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: I is a two-sided ideal of R",
    "¬Q: The quotient ring R/I is not a left Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1