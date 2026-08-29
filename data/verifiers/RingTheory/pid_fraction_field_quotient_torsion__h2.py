import sympy
from sympy import *

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "If R is a principal ideal domain, then the quotient R-module K/R is a torsion module."
    
    The conjecture is false because if R is a field, its fraction field K is R itself,
    so K/R = 0. In many contexts, the zero module is not considered a torsion module 
    (or it's considered trivial), making fields the counterexamples to the strict statement.
    """
    try:
        # H1: R is a principal ideal domain
        # In sympy, domains like ZZ, QQ, and polynomial rings over fields have the is_PID property.
        h1 = bool(witness.is_PID)
    except Exception:
        h1 = False
        
    try:
        # neg_Q: The quotient R-module K/R is NOT a torsion module.
        # For any integral domain that is not a field, K/R is a non-zero torsion module.
        # If R is a field, K = R, so K/R = 0, which is the counterexample.
        neg_q = bool(witness.is_Field)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: The quotient R-module K/R is not a torsion module (e.g., R is a field so K/R = 0)"
]

N_HYP = 1
NEG_Q_INDEX = 1