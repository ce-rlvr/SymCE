import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
# For this field theory conjecture, we use x as the extension generator and t as a transcendental over the base field.
x, t = sp.symbols('x t')

CONDITION_LABELS = [
    "H_1: E is an algebraic extension field of F",
    "¬Q: The extension E/F is not a separable extension"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (p, poly_expr) where:
      - p is a prime integer (the characteristic of the base field F = F_p(t)).
      - poly_expr is a SymPy expression in x and t representing the minimal polynomial of E over F.
    """
    try:
        p, poly_expr = witness
    except Exception:
        return [False, False]
        
    # H_1: E is an algebraic extension field of F
    # This means poly_expr must be an irreducible polynomial in x over F_p(t).
    # Since F_p[t] is a UFD, we can check irreducibility in F_p[x, t].
    h1_ok = False
    try:
        if sp.isprime(p):
            poly = sp.Poly(poly_expr, x, t, domain=sp.GF(p))
            deg_x = poly.degree(x)
            if deg_x > 0:
                coeff, factors = poly.factor_list()
                
                # Find all irreducible factors that have a positive degree in x
                x_factors = []
                for f_poly, m in factors:
                    if f_poly.degree(x) > 0:
                        x_factors.append((f_poly, m))
                
                # For poly_expr to define a field extension, it must have exactly one 
                # irreducible factor involving x, with multiplicity 1, and its degree 
                # in x must match the degree of the original polynomial.
                if len(x_factors) == 1:
                    f_poly, m = x_factors[0]
                    if m == 1 and f_poly.degree(x) == deg_x:
                        h1_ok = True
    except Exception:
        h1_ok = False
        
    # ¬Q: The extension E/F is not a separable extension
    # An irreducible polynomial defines an inseparable extension iff its formal derivative is zero.
    neg_q_ok = False
    try:
        if h1_ok:
            deriv = sp.diff(poly_expr, x)
            deriv_poly = sp.Poly(deriv, x, t, domain=sp.GF(p))
            if deriv_poly.is_zero:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]