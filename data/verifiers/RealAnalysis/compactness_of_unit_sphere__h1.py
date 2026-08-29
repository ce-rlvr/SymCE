import sympy
import math

oo = sympy.oo

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be the dimension n.
    """
    try:
        # H_1: ||.|| is the standard Euclidean norm
        # We accept any valid dimension (positive integer or infinity) or common string representations.
        h1 = False
        if witness == sympy.oo:
            h1 = True
        elif isinstance(witness, (int, float)) and witness >= 1:
            h1 = True
        elif isinstance(witness, str) and witness.lower() in ['oo', 'inf', 'infinity', 'l2', 'l^2', 'l_2']:
            h1 = True
    except Exception:
        h1 = False

    try:
        # ¬Q: S^{n-1} is NOT a compact set in R^n
        # The unit sphere is not compact if and only if the dimension is infinite.
        neg_q = False
        if witness == sympy.oo:
            neg_q = True
        elif isinstance(witness, float) and math.isinf(witness):
            neg_q = True
        elif isinstance(witness, str) and witness.lower() in ['oo', 'inf', 'infinity', 'l2', 'l^2', 'l_2']:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: ||.|| is the standard Euclidean norm",
    "¬Q: S^{n-1} is not a compact set in R^n"
]

N_HYP = 1
NEG_Q_INDEX = 1