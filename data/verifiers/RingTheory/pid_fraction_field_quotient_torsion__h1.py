import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness satisfies the hypothesis and falsifies the conclusion.
    The witness should be a tuple (R, K) where R and K are SymPy domains 
    (e.g., from sympy.polys.domains).
    """
    try:
        R, K = witness
    except Exception:
        return [False, False]

    # H_1: K is the field of fractions of R
    try:
        h1 = (K == R.get_field())
    except Exception:
        h1 = False

    # ¬Q: The quotient R-module K/R is NOT a torsion module
    try:
        if hasattr(R, 'get_field'):
            F = R.get_field()
            # K/R is a torsion module iff K is a subring of the field of fractions of R.
            # For SymPy domains, we check if K's fraction field matches R's fraction field.
            if K == F:
                is_torsion = True
            elif hasattr(K, 'get_field') and K.get_field() == F:
                is_torsion = True
            else:
                is_torsion = False
        else:
            is_torsion = False
            
        neg_q = not is_torsion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "¬Q: The quotient R-module K/R is not a torsion module"
]

N_HYP = 1
NEG_Q_INDEX = 1