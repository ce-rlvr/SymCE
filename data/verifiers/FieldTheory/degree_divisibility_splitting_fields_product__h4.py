import sympy as sp
from sympy.polys.polytools import Poly
import math

x = sp.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        F_domain, f_expr, g_expr, h_expr = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1_ok = F_domain.is_Field
    except Exception:
        h1_ok = False

    try:
        f_poly = Poly(f_expr, x, domain=F_domain)
        h2_ok = f_poly.is_squarefree
    except Exception:
        h2_ok = False

    try:
        g_poly = Poly(g_expr, x, domain=F_domain)
        h_poly = Poly(h_expr, x, domain=F_domain)
        h3_ok = bool(f_poly == g_poly * h_poly)
    except Exception:
        h3_ok = False

    try:
        def splitting_field_degree(poly):
            if poly.degree() <= 1:
                return 1
            if poly.domain.is_FiniteField:
                factors = poly.factor_list()[1]
                deg = 1
                for factor, mult in factors:
                    d = factor.degree()
                    deg = (deg * d) // math.gcd(deg, d)
                return deg
            raise NotImplementedError("Splitting field degree over non-finite fields is not fully supported")

        deg_f = splitting_field_degree(f_poly)
        deg_g = splitting_field_degree(g_poly)
        deg_h = splitting_field_degree(h_poly)
        
        neg_q = (deg_g * deg_h) % deg_f != 0
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a separable polynomial over F",
    "H_3: f = g * h for some polynomials g and h",
    "not Q: The degree of K_f over F does not divide the product of the degrees of K_g and K_h"
]

N_HYP = 3
NEG_Q_INDEX = 3