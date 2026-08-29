import sympy

class GradedRing:
    """
    Mock object to represent a graded ring and its properties for verification.
    """
    def __init__(self, is_commutative=True, is_graded=True, R0_is_Noetherian=True, is_fg_R0_algebra=True):
        self.is_commutative = is_commutative
        self.is_graded = is_graded
        self.R0_is_Noetherian = R0_is_Noetherian
        self.is_fg_R0_algebra = is_fg_R0_algebra

# Standard counterexamples for this conjecture
PolynomialRingInf = GradedRing(is_commutative=True, is_graded=True, R0_is_Noetherian=True, is_fg_R0_algebra=False)
NonNoetherianBaseRing = GradedRing(is_commutative=True, is_graded=True, R0_is_Noetherian=False, is_fg_R0_algebra=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            is_comm = bool(witness.get("is_commutative", False))
            is_graded = bool(witness.get("is_graded", False))
        else:
            is_comm = bool(getattr(witness, "is_commutative", False))
            is_graded = bool(getattr(witness, "is_graded", False))
        h1 = is_comm and is_graded
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            r0_noeth = bool(witness.get("R0_is_Noetherian", False))
            is_fg = bool(witness.get("is_fg_R0_algebra", False))
        else:
            r0_noeth = bool(getattr(witness, "R0_is_Noetherian", False))
            is_fg = bool(getattr(witness, "is_fg_R0_algebra", False))
        neg_q = not (r0_noeth and is_fg)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative graded ring",
    "¬Q: R_0 is not a Noetherian ring or R is not a finitely generated R_0-algebra"
]

N_HYP = 1
NEG_Q_INDEX = 1