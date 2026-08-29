import sympy
from sympy import Poly, Symbol, factor_list, isprime

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        f, b = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: f is a polynomial in ZZ[x]
    try:
        p = Poly(f, x, domain='ZZ')
        h1 = True
    except Exception:
        h1 = False
        
    # H2: b >= 2 is an integer
    try:
        h2 = isinstance(b, (int, sympy.Integer)) and b >= 2
    except Exception:
        h2 = False
        
    # H3: 0 <= a_i < b for all coefficients
    try:
        if h1:
            coeffs = p.all_coeffs()
            h3 = all(0 <= c < b for c in coeffs)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # neg_Q: f is NOT irreducible in ZZ[x]
    try:
        cont, factors = factor_list(f, x, domain='ZZ')
        if len(factors) == 0:
            # Constant polynomial: irreducible iff it is a prime number
            is_irred = isprime(abs(cont))
        elif len(factors) == 1:
            poly, mult = factors[0]
            if mult == 1:
                # Degree >= 1: irreducible iff it is primitive and irreducible over QQ
                is_irred = (abs(cont) == 1)
            else:
                is_irred = False
        else:
            is_irred = False
            
        neg_q = not is_irred
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: f is a polynomial over Z", "H_2: b >= 2 is an integer", "H_3: 0 <= a_i < b for all coefficients", "¬Q: f is reducible over Z"]
N_HYP = 3
NEG_Q_INDEX = 3