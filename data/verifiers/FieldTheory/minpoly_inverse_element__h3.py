import sympy as sp
from sympy import Poly, minpoly, QQ
from sympy.abc import x, y, z, t

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (alpha, f) or an object/dict with these attributes,
    where alpha is an algebraic number and f is a polynomial.
    """
    try:
        if isinstance(witness, dict):
            alpha = witness.get('alpha')
            f = witness.get('f')
        elif hasattr(witness, 'alpha') and hasattr(witness, 'f'):
            alpha = witness.alpha
            f = witness.f
        elif isinstance(witness, tuple) and len(witness) == 2:
            alpha, f = witness
        else:
            return [False, False, False]
            
        if alpha is None or f is None:
            return [False, False, False]
            
        alpha = sp.sympify(alpha)
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field and E/F is a field extension
    # We implicitly work over F = QQ and E = CC, which are valid fields.
    h1 = True
    
    # H_2: alpha in E is a non-zero element that is algebraic over F
    try:
        if alpha == 0:
            h2 = False
        else:
            # Check if alpha is algebraic over QQ by attempting to compute its minimal polynomial
            mp = minpoly(alpha, domain=QQ)
            h2 = True
    except Exception:
        h2 = False
        
    # not Q: The minimal polynomial of alpha^-1 over F is NOT a_0^-1 x^n f(1/x)
    try:
        x_sym_default = sp.Symbol('x')
        if isinstance(f, Poly):
            f_expr = f.as_expr()
            x_sym = f.gen
        else:
            f_expr = sp.sympify(f)
            free_syms = f_expr.free_symbols
            if len(free_syms) == 1:
                x_sym = list(free_syms)[0]
            elif len(free_syms) == 0:
                x_sym = x_sym_default
            else:
                if x_sym_default in free_syms:
                    x_sym = x_sym_default
                else:
                    x_sym = list(free_syms)[0]
                    
        f_poly = Poly(f_expr, x_sym)
        n = f_poly.degree()
        a0 = f_poly.coeff_monomial(1)
        
        if sp.simplify(a0) == 0:
            # If a0 is 0, a_0^-1 is undefined, so the conclusion formula fails.
            neg_q = True
        else:
            # Compute a_0^-1 x^n f(1/x)
            f_1_x = f_expr.subs(x_sym, 1/x_sym)
            expr = sp.expand((1/a0) * (x_sym**n) * f_1_x)
            
            # Compute the actual minimal polynomial of alpha^-1
            mp_inv = sp.expand(minpoly(1/alpha, x_sym))
            
            # Check if they are different
            diff = sp.simplify(expr - mp_inv)
            neg_q = bool(diff != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field and E/F is a field extension",
    "H_2: alpha in E is a non-zero element that is algebraic over F",
    "not Q: The minimal polynomial of alpha^-1 over F is NOT a_0^-1 x^n f(1/x)"
]

N_HYP = 2
NEG_Q_INDEX = 2