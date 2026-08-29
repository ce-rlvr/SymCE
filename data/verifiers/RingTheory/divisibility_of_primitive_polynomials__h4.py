import sympy
from sympy import Poly, div
from sympy.abc import x, y, z

def conditions(witness):
    try:
        f, g = witness
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        
        f_poly = Poly(f, x)
        g_poly = Poly(g, x)
        
        domain = f_poly.domain.unify(g_poly.domain)
        
        # H_1: R is a Unique Factorization Domain
        h1 = bool(domain.is_Exact)
        
        # H_2: F is the field of fractions of R
        F_domain = domain.get_field()
        h2 = bool(F_domain.is_Field)
        
        # H_3: f and g are polynomials in R[x]
        h3 = True
        
        # H_4: f divides g in F[x]
        q_F, r_F = div(g, f, domain=F_domain)
        h4 = bool(r_F == 0)
        
        # ¬Q: f does not divide g in R[x]
        q_R, r_R = div(g, f, domain=domain)
        neg_q = bool(r_R != 0)
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: F is the field of fractions of R",
    "H_3: f and g are polynomials over R",
    "H_4: f divides g in the polynomial ring over F",
    "¬Q: f does not divide g in the polynomial ring over R"
]

N_HYP = 4
NEG_Q_INDEX = 4