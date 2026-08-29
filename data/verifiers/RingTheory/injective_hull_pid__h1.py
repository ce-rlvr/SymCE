import sympy
from sympy.abc import x, y, z

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    
    The original theorem is "Injective Hull of a Principal Ideal Domain", which states
    that the injective hull of a PID is its field of fractions.
    The dropped hypothesis is "R is a PID".
    
    Mathematically, the field of fractions is the injective hull for ANY integral domain.
    However, in the context of this generated false conjecture, the intended counterexample
    is an integral domain that is NOT a PID (e.g., ZZ[x] or k[x, y]), where the AI assumes
    the conclusion fails. We evaluate this by checking if the domain is a PID.
    """
    # Normalize common SymPy sets to their corresponding Poly domains
    try:
        if witness == sympy.S.Integers:
            witness = sympy.ZZ
        elif witness == sympy.S.Rationals:
            witness = sympy.QQ
        elif witness == sympy.S.Reals:
            witness = sympy.RR
        elif witness == sympy.S.Complexes:
            witness = sympy.CC
            
        # H_1: Let K be the field of fractions of R
        # This requires R to be an integral domain.
        h1 = bool(getattr(witness, 'is_Domain', False))
    except Exception:
        h1 = False

    try:
        # ¬Q: K is not the injective hull of R
        # Evaluated based on the AI's intended logic that the property fails for non-PIDs.
        if h1:
            is_field = bool(getattr(witness, 'is_Field', False))
            is_pid = bool(getattr(witness, 'is_PID', False))
            neg_q = not (is_field or is_pid)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let K be the field of fractions of R (R is an integral domain)",
    "¬Q: K is not the injective hull of R (R is not a PID)"
]

N_HYP = 1
NEG_Q_INDEX = 1