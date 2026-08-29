import sympy

def conditions(witness):
    """
    Given a witness (a, n), checks the hypotheses and the negated conclusion.
    """
    try:
        a, n = witness
    except Exception:
        return [False, False, False]
    
    # H_1: a is an integer
    try:
        h1 = isinstance(a, int) or (hasattr(a, 'is_integer') and a.is_integer)
    except Exception:
        h1 = False
        
    # H_2: a is invertible modulo n
    try:
        # Compute the modular inverse of a modulo n
        inv_a = sympy.mod_inverse(a, n)
        h2 = True
    except Exception:
        h2 = False
        
    # Q: -a is invertible modulo n, and its modular inverse is congruent to -(a^-1) mod n
    try:
        # If a is not invertible, Q fails (but H2 would also fail)
        inv_neg_a = sympy.mod_inverse(-a, n)
        
        if n == 0:
            q = (inv_neg_a == -inv_a)
        else:
            # Check congruence modulo n
            q = ((inv_neg_a - (-inv_a)) % n == 0)
    except Exception:
        q = False
        
    return [bool(h1), bool(h2), not bool(q)]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: a is invertible modulo n",
    "not Q: -a is not invertible modulo n, or its modular inverse is not congruent to -(a^-1) mod n"
]

N_HYP = 2
NEG_Q_INDEX = 2