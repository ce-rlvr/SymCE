import sympy
from sympy import Poly, isprime
from sympy.abc import x

# Top-level setup
# Witness is expected to be a tuple (p, P_expr)
# where p is a prime integer representing the characteristic of the field F = GF(p),
# and P_expr is a SymPy expression in x representing the minimal polynomial of alpha over F.

def conditions(witness) -> list[bool]:
    try:
        p, P_expr = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F \subseteq K is a field extension
    # We verify this by checking if P_expr is a valid minimal polynomial 
    # (monic, irreducible, degree >= 1) over GF(p). This implicitly defines 
    # the field extension K = F[x]/(P_expr) and alpha = x.
    try:
        if not isprime(p):
            h1 = False
        else:
            poly_P = Poly(P_expr, x, domain=f'GF({p})')
            h1 = (poly_P.is_irreducible == True) and (poly_P.is_monic == True) and (poly_P.degree() >= 1)
    except Exception:
        h1 = False
        
    # H_2: The characteristic of F is a prime p
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # neg_Q: The minimal polynomial of \alpha over F is NOT of the form x^{p^e} - a
    try:
        if not isprime(p):
            neg_q = False
        else:
            poly_P = Poly(P_expr, x, domain=f'GF({p})')
            d = poly_P.degree()
            
            is_power_of_p = False
            if d > 0:
                temp = d
                while temp % p == 0:
                    temp //= p
                if temp == 1:
                    is_power_of_p = True
                    
            is_binomial_form = True
            for m in poly_P.monoms():
                deg = m[0]
                if deg != d and deg != 0:
                    is_binomial_form = False
                    break
                    
            is_form = is_power_of_p and is_binomial_form
            neg_q = not is_form
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F \\subseteq K is a field extension",
    "H_2: The characteristic of F is a prime p",
    "¬Q: The minimal polynomial of \\alpha over F is NOT of the form x^{p^e} - a"
]

N_HYP = 2
NEG_Q_INDEX = 2