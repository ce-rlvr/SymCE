import sympy
import math

def conditions(witness):
    """
    Checks the remaining hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (a, m, n).
    """
    try:
        # Witness should be a tuple or list of 3 elements: (a, m, n)
        if len(witness) != 3:
            return [False, False]
        a, m, n = witness
    except Exception:
        return [False, False]
        
    # Check Hypothesis 1: a is an integer such that a >= 2
    try:
        h1 = (int(a) == a) and (a >= 2)
    except Exception:
        h1 = False
        
    # Check Negated Conclusion: gcd(a^m - 1, a^n - 1) != a^{gcd(m, n)} - 1
    try:
        a_sym = sympy.S(a)
        m_sym = sympy.S(m)
        n_sym = sympy.S(n)
        
        left = sympy.gcd(a_sym**m_sym - 1, a_sym**n_sym - 1)
        right = a_sym**sympy.gcd(m_sym, n_sym) - 1
        
        neg_q = bool(left != right)
    except Exception:
        # If evaluation fails (e.g., undefined operations), the equality does not hold.
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer such that a >= 2",
    "¬Q: gcd(a^m - 1, a^n - 1) != a^{gcd(m, n)} - 1"
]

N_HYP = 1
NEG_Q_INDEX = 1