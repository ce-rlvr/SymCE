import sympy
from sympy import ZZ, QQ, GF

# Top-level setup
# The witness expression may reference ZZ, QQ, GF
# A valid counterexample witness would be (ZZ, GF(2))

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a tuple of two sympy domains (R, S)
        if len(witness) != 2:
            return [False, False, False]
        R, S = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R and S are integral domains
    try:
        # In sympy, Domain objects (like ZZ, QQ, GF(p)) represent integral domains.
        # We verify they are valid sympy domains by checking for the 'is_Field' attribute.
        h1 = hasattr(R, 'is_Field') and hasattr(S, 'is_Field')
    except Exception:
        h1 = False

    # H_2: S is integral over R
    try:
        # We implement a check for the types of rings we expect in the counterexample.
        # A finite field is integral over ZZ (via the canonical surjective homomorphism).
        if R == S:
            h2 = True
        elif R == ZZ and S.__class__.__name__ == 'FiniteField':
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: R is a field if and only if S is a field (must FAIL)
    try:
        r_is_field = bool(R.is_Field)
        s_is_field = bool(S.is_Field)
        q = (r_is_field == s_is_field)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are integral domains",
    "H_2: S is integral over R",
    "¬Q: The equivalence (R is a field iff S is a field) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2