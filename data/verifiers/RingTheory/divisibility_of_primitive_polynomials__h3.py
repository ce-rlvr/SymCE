import sympy
from sympy import Poly, Symbol
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)) and len(witness) >= 2:
            f, g = witness[-2], witness[-1]
        else:
            return [False, False, False, False, False]
        
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        
        symbols = f.free_symbols | g.free_symbols
        if symbols:
            gen = sorted(list(symbols), key=lambda s: s.name)[0]
        else:
            gen = Symbol('x')
            
    except Exception:
        return [False, False, False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        Poly(f, gen, domain='ZZ')
        h1 = True
    except Exception:
        h1 = False

    # H_2: F is the field of fractions of R
    try:
        Poly(g, gen, domain='QQ')
        h2 = True
    except Exception:
        h2 = False

    # H_3: f is a primitive polynomial
    try:
        p_f = Poly(f, gen, domain='ZZ')
        h3 = (p_f.content() == 1)
    except Exception:
        h3 = False

    # H_4: f divides g in the polynomial ring over F
    try:
        p_f_Q = Poly(f, gen, domain='QQ')
        p_g_Q = Poly(g, gen, domain='QQ')
        q, r = p_g_Q.div(p_f_Q)
        h4 = r.is_zero
    except Exception:
        h4 = False

    # ¬Q: f does not divide g in the polynomial ring over R
    try:
        p_f_Z = Poly(f, gen, domain='ZZ')
        try:
            p_g_Z = Poly(g, gen, domain='ZZ')
            q, r = p_g_Z.div(p_f_Z)
            neg_q = not r.is_zero
        except Exception:
            # If g is not in Z[x], then f cannot divide g in Z[x]
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: F is the field of fractions of R",
    "H_3: f is a primitive polynomial",
    "H_4: f divides g in the polynomial ring over F",
    "¬Q: f does not divide g in the polynomial ring over R"
]

N_HYP = 4
NEG_Q_INDEX = 4