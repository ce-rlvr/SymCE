import sympy
from sympy import Poly, Symbol, ZZ, QQ

# Top-level setup for witness expressions
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Check the hypotheses and negated conclusion for the Monic Polynomial Factorization conjecture.
    """
    try:
        R_domain = ZZ
        K_domain = QQ
        
        if isinstance(witness, dict):
            if 'g' not in witness or 'h' not in witness:
                return [False] * 5
            g = witness['g']
            h = witness['h']
            f = witness.get('f', g * h)
            R_domain = witness.get('R', ZZ)
            K_domain = witness.get('K', QQ)
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                R_domain, K_domain, g, h, f = witness
            elif len(witness) == 4:
                R_domain, K_domain, g, h = witness
                f = g * h
            elif len(witness) == 3:
                g, h, f = witness
            elif len(witness) == 2:
                g, h = witness
                f = g * h
            else:
                return [False] * 5
        else:
            return [False] * 5

        # H_1: R is a unique factorization domain
        try:
            if R_domain == ZZ:
                h1 = True
            else:
                h1 = bool(getattr(R_domain, 'is_UFD', False))
        except Exception:
            h1 = False
            
        # H_2: K is the field of fractions of R
        try:
            if R_domain == ZZ and K_domain == QQ:
                h2 = True
            else:
                h2 = bool(hasattr(R_domain, 'get_field') and K_domain == R_domain.get_field())
        except Exception:
            h2 = False
            
        # H_3: g and h are monic polynomials over K
        try:
            g_poly = Poly(g, x)
            h_poly = Poly(h, x)
            
            try:
                Poly(g, x, domain=K_domain)
                g_in_K = True
            except Exception:
                g_in_K = False
                
            try:
                Poly(h, x, domain=K_domain)
                h_in_K = True
            except Exception:
                h_in_K = False
                
            h3 = bool(g_poly.LC() == 1 and h_poly.LC() == 1 and g_in_K and h_in_K)
        except Exception:
            h3 = False
            
        # H_4: f = gh
        try:
            h4 = bool(sympy.expand(f - g * h) == 0)
        except Exception:
            h4 = False
            
        # ¬Q: g and h do not both have coefficients in R
        try:
            try:
                Poly(g, x, domain=R_domain)
                g_in_R = True
            except Exception:
                g_in_R = False
                
            try:
                Poly(h, x, domain=R_domain)
                h_in_R = True
            except Exception:
                h_in_R = False
                
            neg_q = not (g_in_R and h_in_R)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: K is the field of fractions of R",
    "H_3: g and h are monic polynomials over K",
    "H_4: f = gh",
    "¬Q: g and h do not both have coefficients in R"
]

N_HYP = 4
NEG_Q_INDEX = 4