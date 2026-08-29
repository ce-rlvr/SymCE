import sympy
from sympy import QQ, ZZ

# Top-level setup
# The witness is expected to be a sympy domain such as QQ (the field of rational numbers).
# Fields are Noetherian valuation domains, but they are not discrete valuation rings (DVRs)
# because they have Krull dimension 0 (a DVR must have Krull dimension 1).

def conditions(witness):
    # H_1: R is a valuation domain
    try:
        # Every field is a valuation domain (with the trivial valuation).
        h1 = bool(getattr(witness, 'is_Field', False))
    except Exception:
        h1 = False

    # H_2: R is a Noetherian ring
    try:
        # Fields and principal ideal domains (like ZZ) are Noetherian.
        h2 = bool(getattr(witness, 'is_Field', False) or witness == ZZ)
    except Exception:
        h2 = False

    # ¬Q: R is not a discrete valuation ring (DVR)
    try:
        # A DVR is a local PID that is not a field (it must have exactly one non-zero maximal ideal).
        # Fields have no non-zero maximal ideals, so they are not DVRs.
        # ZZ has infinitely many maximal ideals, so it is not a DVR.
        neg_q = bool(getattr(witness, 'is_Field', False) or witness == ZZ)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a valuation domain",
    "H_2: R is a Noetherian ring",
    "¬Q: R is not a discrete valuation ring (DVR)"
]

N_HYP = 2
NEG_Q_INDEX = 2