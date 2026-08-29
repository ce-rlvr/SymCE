import sympy as sp

# Top-level setup for the witness expressions
x, y = sp.symbols('x y')

def conditions(witness):
    """
    Given a witness, checks if it satisfies the hypotheses and falsifies the conclusion.
    The witness can be a tuple (f, g) or (domain, f, g).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            domain, f, g = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            f, g = witness
            f_poly_temp = sp.Poly(f, x)
            g_poly_temp = sp.Poly(g, x)
            domain = f_poly_temp.domain.unify(g_poly_temp.domain)
            if not domain.is_Field:
                domain = domain.get_field()
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        h1 = bool(domain.is_Field)
    except Exception:
        h1 = False

    # H_2: f(x) and g(x) are non-zero polynomials in F[x]
    try:
        if isinstance(f, sp.Poly):
            f_expr = f.as_expr()
        else:
            f_expr = sp.sympify(f)
            
        if isinstance(g, sp.Poly):
            g_expr = g.as_expr()
        else:
            g_expr = sp.sympify(g)
            
        f_poly = sp.Poly(f_expr, x, domain=domain)
        g_poly = sp.Poly(g_expr, x, domain=domain)
        
        h2_nonzero = not f_poly.is_zero and not g_poly.is_zero
        # Ensure they are polynomials strictly in x (or constants)
        h2_vars = f_expr.free_symbols.issubset({x}) and g_expr.free_symbols.issubset({x})
        
        h2 = bool(h2_nonzero and h2_vars)
    except Exception:
        h2 = False

    # H_3: The greatest common divisor of f(x) and g(x) in F[x] is 1
    try:
        gcd_fg = f_poly.gcd(g_poly)
        # In a field, coprime polynomials have a constant non-zero gcd
        h3 = bool(gcd_fg.degree() == 0 and not gcd_fg.is_zero)
    except Exception:
        h3 = False

    # ¬Q: The polynomial f(x) + y g(x) is reducible in F[x,y]
    try:
        p = f_expr + y * g_expr
        p_poly = sp.Poly(p, x, y, domain=domain)
        
        if p_poly.is_zero:
            neg_q = True
        elif p_poly.degree(x) == 0 and p_poly.degree(y) == 0:
            # Non-zero constants are units in F[x,y], hence not irreducible
            neg_q = True
        else:
            _, factors = p_poly.factor_list()
            # It is reducible if it factors into more than one non-unit polynomial
            total_mult = sum(mult for _, mult in factors)
            neg_q = bool(total_mult > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) and g(x) are non-zero polynomials over F",
    "H_3: The greatest common divisor of f(x) and g(x) over F is 1",
    "¬Q: The polynomial f(x) + y g(x) is reducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3