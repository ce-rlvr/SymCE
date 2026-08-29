import sympy
from sympy import Poly, resultant, degree, GF, sympify, isprime
from sympy.abc import t, x, y

# Top-level setup
# The witness should be a dictionary containing:
# 'p': a prime number (the characteristic of the base field K = F_p(t))
# 'poly_E': an irreducible polynomial in x over K, defining E = K(x)
# 'poly_F': an irreducible polynomial in y over E, defining F = E(y)
# Example counterexample: {'p': 3, 'poly_E': x**3 - t, 'poly_F': y**2 - x}

def conditions(witness):
    try:
        p = int(witness['p'])
        poly_E = sympify(witness['poly_E'])
        poly_F = sympify(witness['poly_F'])
    except Exception:
        return [False, False, False, False]

    # H1: E is an algebraic field extension of K
    try:
        if not isprime(p):
            h1 = False
        else:
            poly_E_mod_p = Poly(poly_E, x, t, domain=GF(p))
            deg_E_x = poly_E_mod_p.degree(x)
            h1 = deg_E_x > 0 and poly_E_mod_p.is_irreducible
    except Exception:
        h1 = False

    # H2: F is an algebraic field extension of E
    try:
        if not isprime(p):
            h2 = False
        else:
            poly_E_mod_p = Poly(poly_E, x, t, domain=GF(p))
            poly_F_mod_p = Poly(poly_F, y, x, t, domain=GF(p))
            deg_F_y = poly_F_mod_p.degree(y)
            res = resultant(poly_E_mod_p.as_expr(), poly_F_mod_p.as_expr(), x)
            res_poly = Poly(res, y, t, domain=GF(p))
            h2 = deg_F_y > 0 and res_poly.is_irreducible
    except Exception:
        h2 = False

    # H3: E/K is a purely inseparable extension
    try:
        if not isprime(p):
            h3 = False
        else:
            poly_E_mod_p = Poly(poly_E, x, t, domain=GF(p))
            deg_E_x = poly_E_mod_p.degree(x)
            q = deg_E_x
            is_power_of_p = True
            if q < 1:
                is_power_of_p = False
            else:
                while q > 1:
                    if q % p != 0:
                        is_power_of_p = False
                        break
                    q = q // p
            
            poly_E_x = Poly(poly_E_mod_p.as_expr(), x)
            terms_ok = True
            for deg_tuple, coeff in poly_E_x.terms():
                d = deg_tuple[0]
                if d != deg_E_x and d != 0:
                    terms_ok = False
                    break
            
            h3 = is_power_of_p and terms_ok
    except Exception:
        h3 = False

    # neg_Q: F/K is NOT a purely inseparable extension
    try:
        if not isprime(p):
            neg_q = False
        else:
            poly_E_mod_p = Poly(poly_E, x, t, domain=GF(p))
            poly_F_mod_p = Poly(poly_F, y, x, t, domain=GF(p))
            res = resultant(poly_E_mod_p.as_expr(), poly_F_mod_p.as_expr(), x)
            res_poly = Poly(res, y, t, domain=GF(p))
            deg_res_y = res_poly.degree(y)
            
            q_res = deg_res_y
            res_is_power_of_p = True
            if q_res < 1:
                res_is_power_of_p = False
            else:
                while q_res > 1:
                    if q_res % p != 0:
                        res_is_power_of_p = False
                        break
                    q_res = q_res // p
            
            res_y = Poly(res_poly.as_expr(), y)
            res_terms_ok = True
            for deg_tuple, coeff in res_y.terms():
                d = deg_tuple[0]
                if d != deg_res_y and d != 0:
                    res_terms_ok = False
                    break
            
            res_is_purely_insep = res_is_power_of_p and res_terms_ok
            neg_q = not res_is_purely_insep
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: E is an algebraic field extension of K",
    "H_2: F is an algebraic field extension of E",
    "H_3: E/K is a purely inseparable extension",
    "¬Q: F/K is not a purely inseparable extension"
]

N_HYP = 3
NEG_Q_INDEX = 3