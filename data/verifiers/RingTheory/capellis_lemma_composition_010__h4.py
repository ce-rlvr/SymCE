import sympy
from sympy import Poly

x = sympy.Symbol('x')
QQ = sympy.QQ
ZZ = sympy.ZZ
GF = sympy.GF

def conditions(witness) -> list[bool]:
    try:
        domain, f, g = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = bool(hasattr(domain, 'is_Field') and domain.is_Field)
    except Exception:
        h1 = False
        
    try:
        f_sym = sympy.sympify(f)
        g_sym = sympy.sympify(g)
        if not isinstance(f_sym, sympy.Expr) or not isinstance(g_sym, sympy.Expr):
            h2 = False
        elif not (f_sym.free_symbols.issubset({x}) and g_sym.free_symbols.issubset({x})):
            h2 = False
        else:
            poly_f = Poly(f_sym, x, domain=domain)
            poly_g = Poly(g_sym, x, domain=domain)
            h2 = True
    except Exception:
        h2 = False
        
    try:
        f_sym = sympy.sympify(f)
        poly_f = Poly(f_sym, x, domain=domain)
        h3 = bool(poly_f.is_irreducible)
    except Exception:
        h3 = False
        
    try:
        f_sym = sympy.sympify(f)
        g_sym = sympy.sympify(g)
        fg = f_sym.subs(x, g_sym)
        poly_fg = Poly(fg, x, domain=domain)
        neg_q = bool(poly_fg.degree() > 0 and not poly_fg.is_irreducible)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f and g are polynomials over K",
    "H_3: f(x) is irreducible over K",
    "¬Q: f(g(x)) is reducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3