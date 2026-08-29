import sympy
from sympy.ntheory import factorint

def conditions(witness):
    """
    Given a witness tuple (p, k), checks if it is a valid counterexample to the conjecture.
    """
    try:
        p, k = witness
    except Exception:
        return [False, False, False]
    
    # H_1: k >= 1 is an integer
    try:
        h1 = isinstance(k, (int, sympy.Integer)) and k >= 1
    except Exception:
        h1 = False
        
    # H_2: p >= 1 is an integer (so p^k is a valid positive integer index for a root of unity)
    try:
        h2 = isinstance(p, (int, sympy.Integer)) and p >= 1
    except Exception:
        h2 = False
        
    # ¬Q: The norm of (1 - zeta_{p^k}) is NOT equal to p
    try:
        if h1 and h2:
            n = int(p)**int(k)
            # The norm of 1 - zeta_n from Q(zeta_n) to Q is Phi_n(1)
            if n == 1:
                norm = 0
            else:
                factors = factorint(n)
                if len(factors) == 1:
                    # If n is a prime power q^m, Phi_n(1) = q
                    norm = list(factors.keys())[0]
                else:
                    # If n has more than one distinct prime factor, Phi_n(1) = 1
                    norm = 1
            neg_q = (norm != p)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: k >= 1 is an integer",
    "H_2: p >= 1 is an integer",
    "¬Q: N(1 - zeta_{p^k}) != p"
]

N_HYP = 2
NEG_Q_INDEX = 2