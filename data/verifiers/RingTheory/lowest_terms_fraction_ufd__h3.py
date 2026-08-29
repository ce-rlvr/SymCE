import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    """
    Given a witness tuple (R, K, x), checks if it is a valid counterexample.
    R: a sympy domain (e.g., ZZ)
    K: a sympy domain (e.g., QQ)
    x: an element to be tested
    """
    try:
        R, K, x_val = witness
    except Exception:
        return [False, False, False]
        
    # Hypothesis 1: R is a Unique Factorization Domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False
        
    # Hypothesis 2: K is the field of fractions of R
    try:
        h2 = bool(K == R.get_field())
    except Exception:
        h2 = False
        
    # Conclusion: There exist coprime elements a, b \in R such that x = a/b
    # In a UFD, any element of its fraction field can be written as a ratio of coprime elements.
    # Therefore, the conclusion holds if and only if x is in K.
    # The negated conclusion holds if and only if x is NOT in K.
    try:
        in_K = (x_val in K)
    except Exception:
        # If checking membership raises an exception (e.g., incompatible types),
        # then x_val is definitely not in K.
        in_K = False
        
    try:
        neg_q = not in_K
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: K is the field of fractions of R",
    "¬Q: There do not exist coprime elements a, b in R such that x = a/b"
]

N_HYP = 2
NEG_Q_INDEX = 2