import sympy
from sympy import cos, pi, minpoly
from sympy.abc import x

# Top-level setup
# (No specific named bindings needed for this field theory conjecture; witnesses are integers)

def conditions(witness):
    """
    Given a witness n, checks if it satisfies the hypotheses and falsifies the conclusion.
    """
    try:
        n = int(witness)
        if n < 1 or n != witness:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: n is a positive integer (required for zeta_n to be a primitive n-th root of unity)
    h1 = True
    
    try:
        # Conclusion: K = Q(zeta_n + zeta_n^-1) is a normal extension of Q.
        # K is the maximal real subfield of the cyclotomic field Q(zeta_n).
        # Since Q(zeta_n) is a Galois extension of Q with an abelian Galois group,
        # every subfield of Q(zeta_n) is also an abelian (and thus normal) extension of Q.
        # Therefore, K is ALWAYS a normal extension of Q for any positive integer n.
        is_normal = True
        
        # neg_Q must be True if the conclusion FAILS.
        neg_q = not is_normal
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: K = Q(zeta_n + zeta_n^-1) is not a normal extension of Q"
]

N_HYP = 1
NEG_Q_INDEX = 1