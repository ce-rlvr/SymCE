import sympy
from sympy import Poly, expand
from sympy.abc import x, y, z
from sympy import ZZ, QQ

def conditions(witness) -> list[bool]:
    try:
        R, K, f, g, h, var = witness
    except Exception:
        return [False, False, False, False, False]
    
    def in_domain(c, dom):
        try:
            return c in dom
        except Exception:
            return False

    # H1: R is a unique factorization domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    # H2: K is the field of fractions of R
    try:
        h2 = bool(K == R.get_field())
    except Exception:
        h2 = False

    # H3: f is a monic polynomial over R
    try:
        p_f = Poly(f, var)
        h3 = bool(p_f.LC() == 1) and all(in_domain(c, R) for c in p_f.coeffs())
    except Exception:
        h3 = False

    # H4: f = gh
    try:
        p_g = Poly(g, var)
        p_h = Poly(h, var)
        eq_check = bool(expand(f - g * h) == 0)
        g_in_K = all(in_domain(c, K) for c in p_g.coeffs())
        h_in_K = all(in_domain(c, K) for c in p_h.coeffs())
        h4 = eq_check and g_in_K and h_in_K
    except Exception:
        h4 = False

    # Neg_Q: g and h do not both lie in polynomials over R
    try:
        try:
            p_g = Poly(g, var)
            g_in_R = all(in_domain(c, R) for c in p_g.coeffs())
        except Exception:
            g_in_R = False
            
        try:
            p_h = Poly(h, var)
            h_in_R = all(in_domain(c, R) for c in p_h.coeffs())
        except Exception:
            h_in_R = False
            
        neg_q = not (g_in_R and h_in_R)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = ["H_1: R is a unique factorization domain", "H_2: K is the field of fractions of R", "H_3: f is a monic polynomial over R", "H_4: f = gh", "not Q: g and h do not both lie in polynomials over R"]
N_HYP = 4
NEG_Q_INDEX = 4