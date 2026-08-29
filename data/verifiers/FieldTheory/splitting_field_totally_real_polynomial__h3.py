import sympy
from sympy import Poly, Symbol, I, QQ, RR, CC
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (f, K) or a dictionary {'f': f, 'K': K},
    where f is a polynomial and K is a field (represented by a domain, a primitive element, or a list of generators).
    """
    if isinstance(witness, dict):
        f = witness.get('f')
        K = witness.get('K')
    else:
        try:
            f, K = witness
        except Exception:
            return [False, False, False]
            
    # H_1: f is a polynomial over Q
    try:
        if hasattr(f, 'free_symbols'):
            free_syms = list(f.free_symbols)
            if len(free_syms) == 1:
                var = free_syms[0]
            elif len(free_syms) == 0:
                var = x
            else:
                var = None
        else:
            var = x
            
        if var is not None:
            poly_f = Poly(f, var)
            h1 = all(c.is_rational for c in poly_f.coeffs())
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: All roots of f in C are real numbers
    try:
        if not h1:
            h2 = False
        else:
            roots = poly_f.all_roots()
            h2 = True
            for r in roots:
                if r.is_real is False:
                    h2 = False
                    break
                elif r.is_real is None:
                    im_part = r.evalf().as_real_imag()[1]
                    if abs(im_part) > 1e-9:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # ¬Q: K is not a subfield of the real numbers R
    try:
        neg_q = False
        if K in [QQ, RR] or str(K) in ['QQ', 'Q', 'R', 'RR', 'Reals', 'Rationals']:
            neg_q = False
        elif K == CC or str(K) in ['CC', 'C', 'Complexes']:
            neg_q = True
        else:
            if hasattr(K, 'ext'):
                gens = [K.ext]
            elif hasattr(K, 'gens'):
                gens = K.gens
            elif isinstance(K, (list, tuple, set)):
                gens = list(K)
            else:
                gens = [K]
            
            for g in gens:
                if hasattr(g, 'as_expr'):
                    g_expr = g.as_expr()
                else:
                    g_expr = g
                
                if hasattr(g_expr, 'is_real'):
                    if g_expr.is_real is False:
                        neg_q = True
                        break
                    elif g_expr.is_real is None:
                        try:
                            im_part = g_expr.evalf().as_real_imag()[1]
                            if abs(im_part) > 1e-9:
                                neg_q = True
                                break
                        except Exception:
                            pass
                else:
                    try:
                        im_part = complex(g_expr).imag
                        if abs(im_part) > 1e-9:
                            neg_q = True
                            break
                    except Exception:
                        pass
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is a polynomial over Q",
    "H_2: All roots of f in C are real numbers",
    "¬Q: K is not a subfield of R"
]

N_HYP = 2
NEG_Q_INDEX = 2