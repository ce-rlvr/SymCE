import sympy

def conditions(witness):
    try:
        m, n = witness
    except Exception:
        return [False, False, False]
    
    # H_1: m is a positive integer
    try:
        h1 = isinstance(m, (int, sympy.Integer)) and type(m) is not bool and m > 0
    except Exception:
        h1 = False
        
    # H_2: m divides n
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and type(n) is not bool and n % m == 0
    except Exception:
        h2 = False
        
    # ¬Q: phi(m) does not divide phi(n)
    try:
        phi_m = sympy.totient(m)
        phi_n = sympy.totient(n)
        q = (phi_n % phi_m == 0)
        neg_q = not q
    except Exception:
        # If totient is undefined (e.g., for n <= 0), the conclusion fails.
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: m divides n",
    "¬Q: phi(m) does not divide phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2