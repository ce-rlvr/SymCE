import sympy
from sympy import Symbol, Poly, div
from sympy import QQ, ZZ, RR, CC, GF
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        F, f, g = witness
    except Exception:
        return [False, False, False]
        
    # H1: Let F be a field.
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    # Determine the variable of the polynomials
    try:
        symbols = set()
        if hasattr(f, 'free_symbols'):
            symbols.update(f.free_symbols)
        if hasattr(g, 'free_symbols'):
            symbols.update(g.free_symbols)
        if len(symbols) == 1:
            var = list(symbols)[0]
        elif len(symbols) == 0:
            var = Symbol('x')
        else:
            x_sym = Symbol('x')
            if x_sym in symbols:
                var = x_sym
            else:
                var = list(symbols)[0]
    except Exception:
        var = Symbol('x')
        
    # H2: Let g(x) be a non-zero polynomial.
    try:
        g_poly = Poly(g, var)
        h2 = not g_poly.is_zero
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion fails (unique q, r in F[x] do not exist)
    try:
        try:
            f_poly = Poly(f, var, domain=F)
            f_is_poly = True
        except Exception:
            f_is_poly = False
            
        if not f_is_poly:
            neg_q = True
        else:
            try:
                q, r = div(f, g, var, domain=F)
                q_poly = Poly(q, var, domain=F)
                r_poly = Poly(r, var, domain=F)
                g_poly_F = Poly(g, var, domain=F)
                
                if r_poly.is_zero or r_poly.degree() < g_poly_F.degree():
                    neg_q = False
                else:
                    neg_q = True
            except Exception:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: g(x) is a non-zero polynomial",
    "¬Q: Unique q(x) and r(x) in the polynomial ring do not exist"
]

N_HYP = 2
NEG_Q_INDEX = 2