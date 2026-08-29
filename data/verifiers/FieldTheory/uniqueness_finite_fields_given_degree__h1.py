import sympy
import sympy.ntheory

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            n = witness.get('n')
        else:
            p, n = witness
    except Exception:
        return [False, False]
        
    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False
        
    # ¬Q: There does NOT exist exactly one field extension of F_p of degree n
    # This happens if F_p is not a field (i.e., p is not a prime power)
    try:
        if isinstance(p, (int, sympy.Integer)) and p >= 2:
            factors = sympy.ntheory.factorint(p)
            is_prime_power = (len(factors) == 1)
            neg_q = not is_prime_power
        else:
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: F_p does not have exactly one field extension of degree n (e.g., p is not a prime power)"
]

N_HYP = 1
NEG_Q_INDEX = 1