import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y

def conditions(witness):
    """
    Check if the witness is a counterexample to the false conjecture:
    "Let R be a Unique Factorization Domain. Then there exist elements a, b in R 
    such that their greatest common divisor is a unit, but the principal ideals 
    (a) and (b) are not comaximal."
    
    The negation of the conclusion is that for all a, b in R, if gcd(a,b) is a unit, 
    then (a) + (b) = R. In a UFD, this property is equivalent to R being a 
    Principal Ideal Domain (PID).
    """
    try:
        # H_1: R is a Unique Factorization Domain
        h1_ok = bool(getattr(witness, 'is_UFD', False))
    except Exception:
        h1_ok = False

    try:
        # ¬Q: The conclusion fails if every pair of coprime elements generates the unit ideal.
        # For a UFD, this is equivalent to the ring being a Principal Ideal Domain (PID).
        neg_q_ok = bool(getattr(witness, 'is_PID', False))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "¬Q: For all coprime a, b in R, (a) and (b) are comaximal (R is a PID)"
]

N_HYP = 1
NEG_Q_INDEX = 1