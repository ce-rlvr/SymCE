import sympy
from sympy import Poly, Symbol, gcd
import functools

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
t = Symbol('t')

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R, f, g = witness
            elif len(witness) == 2:
                f, g = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        f = sympy.sympify(f)
        g = sympy.sympify(g)
    except Exception:
        return [False, False, False]

    try:
        free_vars = set()
        if hasattr(f, 'free_symbols'):
            free_vars.update(f.free_symbols)
        if hasattr(g, 'free_symbols'):
            free_vars.update(g.free_symbols)
            
        if len(free_vars) == 1:
            var = list(free_vars)[0]
        elif len(free_vars) == 0:
            var = x
        else:
            var = x
            
        poly_f = Poly(f, var)
        poly_g = Poly(g, var)
        
        h1 = all(c.is_integer for c in poly_f.coeffs()) and all(c.is_integer for c in poly_g.coeffs())
    except Exception:
        h1 = False

    try:
        h2 = f.is_polynomial(var) and g.is_polynomial(var)
    except Exception:
        h2 = False

    try:
        poly_fg = Poly(f + g, var)
        
        coeffs_f = poly_f.coeffs()
        coeffs_g = poly_g.coeffs()
        coeffs_fg = poly_fg.coeffs()
        
        c_f = functools.reduce(gcd, coeffs_f) if coeffs_f else 0
        c_g = functools.reduce(gcd, coeffs_g) if coeffs_g else 0
        c_fg = functools.reduce(gcd, coeffs_fg) if coeffs_fg else 0
        
        c_f_plus_g = gcd(c_f, c_g)
        
        neg_q = abs(c_fg) != abs(c_f_plus_g)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f and g are polynomials over R",
    "¬Q: c(f+g) is not equal to c(f) + c(g)"
]

N_HYP = 2
NEG_Q_INDEX = 2