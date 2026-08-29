import math
import sympy
from sympy.ntheory import factorint

# Top-level setup
# (No specific named objects required for this Field Theory conjecture)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple containing (q, m, n).
    """
    try:
        # Extract the last 3 elements to handle both (q, m, n) and (F, q, m, n)
        q, m, n = witness[-3:]
    except Exception:
        return [False, False, False]
    
    # H_1: F_q is a finite field with q elements
    # This implies q must be a prime power.
    try:
        q_val = int(q)
        if q_val >= 2:
            factors = factorint(q_val)
            h1 = (len(factors) == 1)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: m and n are positive integers
    try:
        m_val = int(m)
        n_val = int(n)
        h2 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and (m_val > 0) and (n_val > 0)
    except Exception:
        h2 = False
        
    # ¬Q: The intersection F_{q^m} \cap F_{q^n} is exactly the field F_{q^{\gcd(m,n)}}
    # The conjecture dropped the hypothesis that F_{q^m} and F_{q^n} are subfields of a common overfield.
    # Without a common overfield, the intersection of the abstract extensions F_{q^m} and F_{q^n} 
    # is just their common base field, F_q.
    # The conclusion claims the intersection is F_{q^{\gcd(m,n)}}.
    # This claim is false if and only if \gcd(m, n) > 1 and m != n.
    try:
        m_val = int(m)
        n_val = int(n)
        neg_q = (math.gcd(m_val, n_val) > 1) and (m_val != n_val)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: m and n are positive integers",
    "¬Q: The intersection F_{q^m} \\cap F_{q^n} is not exactly the field F_{q^{\\gcd(m,n)}}"
]

N_HYP = 2
NEG_Q_INDEX = 2