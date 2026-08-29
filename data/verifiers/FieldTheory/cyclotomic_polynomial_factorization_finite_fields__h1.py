import math
from sympy import cyclotomic_poly, factor_list, GF, Poly
from sympy.abc import x
from sympy.ntheory import n_order, factorint

# The witness is expected to be a tuple of integers: (q, n, d)

def conditions(witness):
    try:
        q, n, d = witness
    except Exception:
        return [False, False, False]
        
    # H1: n is a positive integer such that gcd(q, n) == 1
    try:
        h1 = (isinstance(n, int) and n > 0 and isinstance(q, int) and math.gcd(q, n) == 1)
    except Exception:
        h1 = False
        
    # H2: d is the multiplicative order of q modulo n
    try:
        if h1:
            expected_d = n_order(q, n)
            h2 = (d == expected_d)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The n-th cyclotomic polynomial \Phi_n(x) factors over \mathbb{F}_q into a product 
    # of distinct monic irreducible polynomials, all of which have degree exactly d.
    try:
        # If q is not a prime power, the finite field F_q does not exist,
        # so the conclusion trivially fails.
        if not isinstance(q, int) or q < 2 or len(factorint(q)) != 1:
            concl = False
        else:
            Fq = GF(q)
            poly = cyclotomic_poly(n, x)
            factors = factor_list(poly, domain=Fq)
            
            concl = True
            if factors[0] not in (1, getattr(Fq, 'one', 1)):
                concl = False
                
            for f_expr, mult in factors[1]:
                if mult != 1:
                    concl = False
                    break
                f_poly = Poly(f_expr, x, domain=Fq)
                if f_poly.degree() != d:
                    concl = False
                    break
                if f_poly.LC() not in (1, getattr(Fq, 'one', 1)):
                    concl = False
                    break
    except Exception:
        concl = False
        
    neg_q = not concl
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer such that gcd(q, n) == 1",
    "H_2: d is the multiplicative order of q modulo n",
    "¬Q: Phi_n(x) does not factor over F_q into distinct monic irreducible polynomials of degree exactly d"
]

N_HYP = 2
NEG_Q_INDEX = 2