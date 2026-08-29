import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Expected witness format: (poly_gamma, poly_alpha, P)
    - poly_gamma: minimal polynomial of gamma over Q, defining the extension E = Q(gamma)
    - poly_alpha: minimal polynomial of alpha over Q
    - P: polynomial such that alpha = P(gamma)
    """
    try:
        if not isinstance(witness, (list, tuple)):
            return [False, False, False]
            
        if len(witness) == 3:
            poly_gamma_expr, poly_alpha_expr, P_expr = witness
        elif len(witness) == 4:
            poly_gamma_expr, poly_alpha_expr, P_expr, _ = witness
        else:
            return [False, False, False]
            
        poly_gamma_expr = sympy.sympify(poly_gamma_expr)
        poly_alpha_expr = sympy.sympify(poly_alpha_expr)
        P_expr = sympy.sympify(P_expr)
        
        symbols = (poly_gamma_expr.free_symbols | poly_alpha_expr.free_symbols | P_expr.free_symbols)
        symbols = {s for s in symbols if isinstance(s, sympy.Symbol)}
        
        if len(symbols) > 1:
            return [False, False, False]
        elif len(symbols) == 1:
            s = list(symbols)[0]
            poly_gamma_expr = poly_gamma_expr.subs(s, x)
            poly_alpha_expr = poly_alpha_expr.subs(s, x)
            P_expr = P_expr.subs(s, x)
            
        poly_gamma = Poly(poly_gamma_expr, x, domain='QQ')
        poly_alpha = Poly(poly_alpha_expr, x, domain='QQ')
        P = Poly(P_expr, x, domain='QQ')
        
        h1 = poly_gamma.is_irreducible
        
        comp_expr = poly_alpha.as_expr().subs(x, P.as_expr())
        rem = sympy.rem(comp_expr, poly_gamma.as_expr(), x, domain='QQ')
        h2 = poly_alpha.is_irreducible and (rem == 0)
        
        deg_E = poly_gamma.degree()
        deg_alpha = poly_alpha.degree()
        
        neg_q = (deg_alpha != 1) and (deg_alpha != deg_E)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: E/F is a field extension",
    "H_2: alpha is an element of E",
    "not Q: The degree of the minimal polynomial of alpha over F is neither 1 nor p"
]

N_HYP = 2
NEG_Q_INDEX = 2