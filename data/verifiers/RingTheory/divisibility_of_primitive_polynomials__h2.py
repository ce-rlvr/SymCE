import sympy as sp
from sympy.abc import x, y, z

ZZ = sp.ZZ
QQ = sp.QQ

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f and g are polynomials over R",
    "H_3: f is a primitive polynomial",
    "H_4: f divides g in the polynomial ring over F",
    "not Q: f does not divide g in the polynomial ring over R"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    if not isinstance(witness, (tuple, list)):
        return [False] * 5
    
    if len(witness) == 2:
        f, g = witness
        F_val = None
    elif len(witness) == 3:
        f, g, F_val = witness
    elif len(witness) == 4:
        _, f, g, F_val = witness
    else:
        return [False] * 5

    try:
        free_syms = set()
        if hasattr(f, 'free_symbols'):
            free_syms.update(f.free_symbols)
        if hasattr(g, 'free_symbols'):
            free_syms.update(g.free_symbols)
        
        if free_syms:
            var = sorted(list(free_syms), key=lambda s: str(s))[0]
        else:
            var = x
    except Exception:
        var = x

    # H_2: f and g are polynomials over R
    try:
        f_poly = sp.Poly(f, var)
        g_poly = sp.Poly(g, var)
        R_domain = f_poly.domain.unify(g_poly.domain)
        f_poly = sp.Poly(f, var, domain=R_domain)
        g_poly = sp.Poly(g, var, domain=R_domain)
        h2 = True
    except Exception:
        h2 = False

    # H_1: R is a Unique Factorization Domain
    try:
        if h2:
            h1 = getattr(R_domain, 'is_UFD', True)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_3: f is a primitive polynomial
    try:
        if h2:
            prim = f_poly.is_primitive
            if callable(prim):
                h3 = bool(prim())
            else:
                h3 = bool(prim)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: f divides g in the polynomial ring over F
    h4 = False
    try:
        if h2:
            if F_val is not None:
                if isinstance(F_val, int) or (hasattr(F_val, 'is_integer') and F_val.is_integer):
                    F_domain = sp.GF(int(F_val))
                else:
                    F_domain = F_val
                f_F = sp.Poly(f, var, domain=F_domain)
                g_F = sp.Poly(g, var, domain=F_domain)
                if not f_F.is_zero:
                    q, r = g_F.div(f_F)
                    h4 = r.is_zero
            else:
                # Try field of fractions first
                try:
                    F_domain = R_domain.get_field()
                    f_F = sp.Poly(f, var, domain=F_domain)
                    g_F = sp.Poly(g, var, domain=F_domain)
                    if not f_F.is_zero:
                        q, r = g_F.div(f_F)
                        if r.is_zero:
                            h4 = True
                except Exception:
                    pass
                
                # If not, try finite fields
                if not h4:
                    for p in sp.primerange(2, 100):
                        try:
                            F_domain = sp.GF(p)
                            f_F = sp.Poly(f, var, domain=F_domain)
                            if f_F.is_zero:
                                continue
                            g_F = sp.Poly(g, var, domain=F_domain)
                            q, r = g_F.div(f_F)
                            if r.is_zero:
                                h4 = True
                                break
                        except Exception:
                            continue
    except Exception:
        h4 = False

    # ¬Q: f does not divide g in the polynomial ring over R
    neg_q = False
    try:
        if h2:
            if not f_poly.is_zero:
                q, r = g_poly.div(f_poly)
                neg_q = not r.is_zero
            else:
                neg_q = not g_poly.is_zero
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]