import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims that any ring F has an algebraically closed algebraic extension.
    This is true if and only if F is a field. Thus, the conclusion fails (neg_Q is True)
    if and only if F is not a field.
    """
    try:
        if witness == sympy.S.Integers:
            neg_q = True
        elif witness in (sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals):
            neg_q = False
        elif hasattr(witness, 'is_Field'):
            neg_q = not bool(witness.is_Field)
        elif hasattr(witness, 'is_field'):
            neg_q = not bool(witness.is_field)
        else:
            # If we cannot determine, default to False to avoid false positives
            neg_q = False
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: F does not have an algebraically closed algebraic extension (F is not a field)"
]

N_HYP = 0
NEG_Q_INDEX = 0