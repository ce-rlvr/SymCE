import sympy
from sympy import Symbol, Poly, simplify, expand

# Top-level setup
x = Symbol('x')
y = Symbol('y')
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    """
    if isinstance(witness, dict):
        F = witness.get('F')
        alpha = witness.get('alpha')
        beta = witness.get('beta')
        f = witness.get('f')
        g = witness.get('g')
        R = witness.get('R')
    else:
        F = getattr(witness, 'F', None)
        alpha = getattr(witness, 'alpha', None)
        beta = getattr(witness, 'beta', None)
        f = getattr(witness, 'f', None)
        g = getattr(witness, 'g', None)
        R = getattr(witness, 'R', None)

    # Find the variable used in the polynomials
    var = x
    for expr in [f, g, R]:
        if hasattr(expr, 'free_symbols') and expr.free_symbols:
            symbols = list(expr.free_symbols)
            if symbols:
                var = symbols[0]
                break

    # H_1: F is a field
    try:
        H1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        H1 = False

    # H_2: alpha and beta are algebraic elements over F
    try:
        # If they are algebraic, minpoly will succeed and return a polynomial
        sympy.minpoly(alpha, var)
        sympy.minpoly(beta, var)
        H2 = True
    except Exception:
        H2 = False

    # H_3: f(x) and g(x) are the minimal polynomials of alpha and beta over F
    try:
        f_poly = Poly(f, var, domain=F)
        g_poly = Poly(g, var, domain=F)
        
        f_monic = (f_poly.LC() == 1)
        g_monic = (g_poly.LC() == 1)
        
        f_val = simplify(expand(f_poly.as_expr().subs(var, alpha)))
        g_val = simplify(expand(g_poly.as_expr().subs(var, beta)))
        
        f_root = (f_val == 0)
        g_root = (g_val == 0)
        
        f_irred = f_poly.is_irreducible
        g_irred = g_poly.is_irreducible
        
        H3 = bool(f_monic and g_monic and f_root and g_root and f_irred and g_irred)
    except Exception:
        H3 = False

    # neg_Q: The minimal polynomial of alpha + beta over F does NOT divide R(x)
    try:
        minpoly_sum = sympy.minpoly(alpha + beta, var)
        minpoly_sum_poly = Poly(minpoly_sum, var, domain=F)
        R_poly = Poly(R, var, domain=F)
        
        rem = R_poly % minpoly_sum_poly
        neg_Q = not rem.is_zero
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha and beta are algebraic elements over F",
    "H_3: f(x) and g(x) are the minimal polynomials of alpha and beta over F",
    "not Q: The minimal polynomial of alpha + beta over F does NOT divide R(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3