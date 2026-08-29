import sympy

# Top-level setup
# (No specific named objects needed for this parameter check)

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (p, n), checks if it is a valid counterexample to the false conjecture.
    """
    try:
        p, n = witness
    except Exception:
        return [False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    # ¬Q: There does NOT exist exactly one field extension of F_p of degree n up to isomorphism.
    # The conclusion Q holds if and only if n is a positive integer (n >= 1).
    # If n is not a positive integer (e.g., n <= 0, or n is a fraction), there are 0 such extensions.
    try:
        n_sym = sympy.S(n)
        if n_sym.is_integer and n_sym >= 1:
            q = True
        else:
            q = False
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: There does not exist exactly one field extension of F_p of degree n up to isomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1