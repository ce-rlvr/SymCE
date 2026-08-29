import sympy
from sympy import Poly, factor_list
from sympy.abc import x

def conditions(witness):
    try:
        p, f = witness
    except Exception:
        return [False, False, False, False, False]
    
    try:
        if not isinstance(p, (int, sympy.Integer)):
            h1 = False
        else:
            poly_f = Poly(f, x, domain='ZZ')
            h1 = True
    except Exception:
        h1 = False

    try:
        h2 = sympy.isprime(p)
    except Exception:
        h2 = False

    try:
        poly_f = Poly(f, x, domain='ZZ')
        h3 = poly_f.degree() >= 1
    except Exception:
        h3 = False

    try:
        f_mod_p = Poly(f, x, modulus=p)
        h4 = f_mod_p.degree() >= 1 and f_mod_p.is_irreducible
    except Exception:
        h4 = False

    try:
        _, factors = factor_list(f, domain='ZZ')
        pos_deg_factors_count = sum(mult for fac, mult in factors if Poly(fac, x).degree() >= 1)
        neg_q = pos_deg_factors_count >= 2
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: D is a unique factorization domain",
    "H_2: P is a prime ideal of D",
    "H_3: f is a non-constant polynomial over D",
    "H_4: The image of f mod P is irreducible",
    "¬Q: f can be factored into two polynomials of positive degree over D"
]

N_HYP = 4
NEG_Q_INDEX = 4