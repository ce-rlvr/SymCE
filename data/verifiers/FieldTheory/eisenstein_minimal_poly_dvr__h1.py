import sympy
from sympy import Symbol, Poly, simplify, QQ, ZZ, sqrt, I, oo, Rational, Integer

# Top-level setup for witness expressions
x = Symbol('x')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness must be a dictionary providing:
      - 'v': a callable representing the discrete valuation function v
      - 'pi': the uniformizer element
      - 'f': the Eisenstein polynomial (as a sympy Expr or Poly in x)
      - 'alpha': a root of f(x)
      - 'F': the field F (e.g., a sympy Domain like QQ.algebraic_field(sqrt(2)))
      - 'g': a polynomial in F[x] of lower degree than f such that g(alpha) = 0, 
             acting as a certificate that f is not the minimal polynomial over F.
    """
    try:
        v = witness['v']
        pi = witness['pi']
        f = witness['f']
        alpha = witness['alpha']
        F = witness['F']
        g = witness['g']
    except (TypeError, KeyError):
        return [False, False, False, False]
        
    # H_1: pi is a uniformizer for O_v
    try:
        h1 = bool(v(pi) == 1)
    except Exception:
        h1 = False
        
    # H_2: f(x) is an Eisenstein polynomial with respect to pi
    try:
        if isinstance(f, Poly):
            f_expr = f.as_expr()
            f_poly = f
        else:
            f_expr = f
            f_poly = Poly(f_expr, x)
            
        coeffs = f_poly.all_coeffs()
        n = f_poly.degree()
        
        # Eisenstein criteria: monic, degree >= 1, v(a_i) >= 1 for i < n, v(a_0) == 1
        if n >= 1 and coeffs[0] == 1:
            vals_ge_1 = all(v(c) >= 1 for c in coeffs[1:])
            val_a0_eq_1 = (v(coeffs[-1]) == 1)
            h2 = bool(vals_ge_1 and val_a0_eq_1)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H_3: alpha is a root of f(x) in some extension field of F
    try:
        h3 = bool(simplify(f_expr.subs(x, alpha)) == 0)
    except Exception:
        h3 = False
        
    # ¬Q: f(x) is not the minimal polynomial of alpha over F
    # We verify this by checking the provided certificate polynomial g(x)
    try:
        if isinstance(g, Poly):
            g_expr = g.as_expr()
            g_poly = g
        else:
            g_expr = g
            g_poly = Poly(g_expr, x)
            
        g_coeffs = g_poly.all_coeffs()
        
        g_is_valid = True
        if g_poly.is_zero:
            g_is_valid = False
        elif bool(simplify(g_expr.subs(x, alpha)) != 0):
            g_is_valid = False
        elif g_poly.degree() >= f_poly.degree():
            g_is_valid = False
        elif not all(c in F for c in g_coeffs):
            g_is_valid = False
            
        neg_q = g_is_valid
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: pi is a uniformizer for O_v",
    "H_2: f(x) is an Eisenstein polynomial with respect to pi",
    "H_3: alpha is a root of f(x) in some extension field of F",
    "¬Q: f(x) is not the minimal polynomial of alpha over F"
]

N_HYP = 3
NEG_Q_INDEX = 3