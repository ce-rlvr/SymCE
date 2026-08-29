import sympy as sp
from sympy import Poly, QQ, RR, CC, ZZ, Symbol, GF

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, g, K = witness
            elif len(witness) == 2:
                f, g = witness
                K = QQ
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        free_syms = set()
        if hasattr(f, 'free_symbols'):
            free_syms.update(f.free_symbols)
        if hasattr(g, 'free_symbols'):
            free_syms.update(g.free_symbols)
        
        if len(free_syms) > 1:
            h1 = False
        else:
            if len(free_syms) == 1:
                var = list(free_syms)[0]
            else:
                var = x
            f_poly = Poly(f, var, domain=K)
            g_poly = Poly(g, var, domain=K)
            h1 = True
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            gcd_fg = f_poly.gcd(g_poly)
            
            left_side = (gcd_fg.degree() == 0) and not gcd_fg.is_zero
            
            if gcd_fg.is_zero:
                has_root_in_K = True
            elif K == CC:
                has_root_in_K = (gcd_fg.degree() > 0)
            elif K == RR:
                try:
                    rts = sp.real_roots(gcd_fg.as_expr())
                    has_root_in_K = len(rts) > 0
                except Exception:
                    rts = sp.roots(gcd_fg.as_expr(), var)
                    has_root_in_K = any(r.is_real for r in rts.keys())
            else:
                rts = gcd_fg.ground_roots()
                has_root_in_K = len(rts) > 0
                
            right_side = not has_root_in_K
            
            neg_q = (left_side != right_side)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f and g are polynomials",
    "¬Q: gcd is non-zero constant iff no common roots fails"
]

N_HYP = 1
NEG_Q_INDEX = 1