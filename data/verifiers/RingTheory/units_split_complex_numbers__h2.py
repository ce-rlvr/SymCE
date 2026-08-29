import sympy as sp

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: a, b in R",
    "¬Q: The element a + bj is a unit in S if and only if a^2 - b^2 is a unit in R fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The witness should be a tuple (R, a, b) where R is a SymPy ring/domain.
    """
    try:
        R, a, b = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        # Check if R is a commutative ring with identity
        h1 = hasattr(R, 'is_commutative') and R.is_commutative and hasattr(R, 'has_Identity')
        if not h1:
            # Fallback for SymPy domains like ZZ, QQ
            h1 = hasattr(R, 'is_ring') and R.is_ring
    except Exception:
        h1 = False

    # H_2: a, b \in R
    try:
        h2 = (a in R) and (b in R)
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails
    # The conclusion is: a + bj is a unit in S iff a^2 - b^2 is a unit in R.
    # In the context of the dropped hypothesis (e.g., R is a field or S is over a larger field like R),
    # S is typically the split-complex numbers over the field of fractions of R (or R itself).
    # If S is over the field of fractions (e.g., R=ZZ, S over QQ), a+bj is a unit in S iff a^2 - b^2 != 0.
    # We check if the equivalence fails.
    try:
        norm = a**2 - b**2
        
        # Is a^2 - b^2 a unit in R?
        if hasattr(R, 'is_unit'):
            is_unit_R = R.is_unit(norm)
        else:
            # Fallback for ZZ
            is_unit_R = (norm == 1 or norm == -1)
            
        # Is a + bj a unit in S?
        # If S is the split-complex numbers over the field of fractions of R, it's a unit iff norm != 0
        is_unit_S = (norm != 0)
        
        neg_q = (is_unit_S != is_unit_R)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]