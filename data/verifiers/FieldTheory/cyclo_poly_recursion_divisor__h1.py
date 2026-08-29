import sympy
from sympy import Symbol
from sympy.polys import cyclotomic_poly

x = Symbol('x')

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p divides n",
    "¬Q: \\Phi_{pn}(x) != \\Phi_n(x^p) or is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        p, n = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    try:
        if h1:
            h2 = bool(n % p == 0)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        # Evaluate the cyclotomic polynomials.
        # If n <= 0, cyclotomic_poly will raise a ValueError,
        # meaning the equation is undefined (and thus the conclusion fails).
        lhs = cyclotomic_poly(int(p * n), x)
        rhs = cyclotomic_poly(int(n), x**int(p))
        concl = bool(sympy.expand(lhs - rhs) == 0)
    except Exception:
        concl = False
        
    neg_q = not concl
    
    return [h1, h2, neg_q]