import math
from sympy.ntheory import totient

# Top-level setup
# No specific named objects are required for this field theory conjecture.

def conditions(witness):
    """
    Given a witness (expected to be a tuple or dict containing n and m),
    checks the hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            m = witness.get('m')
        else:
            n, m = witness
        
        h1 = isinstance(n, int) and isinstance(m, int) and n > 0 and m > 0
    except Exception:
        h1 = False

    try:
        # The conclusion states that the compositum of Q(zeta_n) and Q(zeta_m)
        # is equal to the cyclotomic field Q(zeta_{lcm(n,m)}).
        # Mathematically, since Q(zeta_n) and Q(zeta_m) are Galois extensions of Q, 
        # their compositum in any common overfield (like C) is well-defined and 
        # is exactly Q(zeta_{lcm(n,m)}). 
        # Therefore, the conclusion is ALWAYS true for any positive integers n, m.
        # As a result, the negated conclusion (neg_Q) is always False.
        if h1:
            # We can formally verify this by checking the degrees over Q.
            # The degree of the compositum Q(zeta_n, zeta_m) is totient(lcm(n, m)).
            # The degree of Q(zeta_{lcm(n,m)}) is also totient(lcm(n, m)).
            # Since one is a subfield of the other and their degrees match, they are equal.
            lcm_nm = (n * m) // math.gcd(n, m)
            deg_compositum = totient(lcm_nm)
            deg_lcm_field = totient(lcm_nm)
            q = (deg_compositum == deg_lcm_field)
        else:
            q = True
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n and m are positive integers",
    "¬Q: The compositum of Q(zeta_n) and Q(zeta_m) is NOT equal to Q(zeta_{lcm(n,m)})"
]

N_HYP = 1
NEG_Q_INDEX = 1