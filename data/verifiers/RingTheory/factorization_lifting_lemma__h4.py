import sympy
from sympy import abc

x, y, z = sympy.symbols('x y z')
ZZ = sympy.S.Integers
QQ = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 5:
            R, F, f, G, H = witness
        elif len(witness) == 3:
            f, G, H = witness
        else:
            return [False, False, False, False]
            
        f_expr = sympy.sympify(f)
        G_expr = sympy.sympify(G)
        H_expr = sympy.sympify(H)
        
        symbols = f_expr.free_symbols | G_expr.free_symbols | H_expr.free_symbols
        if len(symbols) > 1:
            return [False, False, False, False]
        
        gen = list(symbols)[0] if symbols else sympy.Symbol('x')
        
        f_poly = sympy.Poly(f_expr, gen)
        G_poly = sympy.Poly(G_expr, gen)
        H_poly = sympy.Poly(H_expr, gen)
        
    except Exception:
        return [False, False, False, False]

    try:
        h1 = f_poly.domain.is_ZZ or f_poly.domain.is_QQ
    except Exception:
        h1 = False

    try:
        h2 = (G_poly.domain.is_ZZ or G_poly.domain.is_QQ) and (H_poly.domain.is_ZZ or H_poly.domain.is_QQ)
    except Exception:
        h2 = False

    try:
        h3 = True
    except Exception:
        h3 = False

    try:
        if G_poly.is_zero or H_poly.is_zero:
            neg_q = not f_poly.is_zero
        elif f_poly.is_zero:
            neg_q = True
        else:
            prod = G_poly * H_poly
            if f_poly.degree() != prod.degree():
                neg_q = True
            else:
                is_prop = (f_poly * prod.LC()) == (prod * f_poly.LC())
                neg_q = not is_prop
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: F is the field of fractions of R",
    "H_3: f is a polynomial over R",
    "¬Q: There do not exist g and h over R and non-zero a and b in F such that G=ag, H=bh, f=gh"
]

N_HYP = 3
NEG_Q_INDEX = 3