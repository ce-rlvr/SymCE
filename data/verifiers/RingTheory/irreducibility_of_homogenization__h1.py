import sympy

# Top-level setup
x0, x1, x2, x3, x4 = sympy.symbols('x0 x1 x2 x3 x4')

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The witness is expected to be a tuple (f, d) where f is a polynomial and d is the degree for homogenization.
    """
    try:
        if isinstance(witness, tuple) or isinstance(witness, list):
            f, d = witness
        elif isinstance(witness, dict):
            f = witness.get('f')
            d = witness.get('d')
        else:
            f = witness
            f_poly = sympy.Poly(f)
            d = f_poly.total_degree()
            
        f = sympy.sympify(f)
        d = int(d)
    except Exception:
        return [False, False, False]

    # H1: f is a non-zero polynomial of degree d
    try:
        if f == 0:
            h1 = False
        else:
            poly_f = sympy.Poly(f)
            deg_f = poly_f.total_degree()
            # The polynomial must be valid and its actual degree should not exceed d
            h1 = (deg_f <= d)
    except Exception:
        h1 = False

    # H2: F is the homogenization of f
    try:
        free_vars = list(f.free_symbols)
        homog_var = sympy.Symbol('x0')
        if homog_var in free_vars:
            homog_var = sympy.Symbol('X0_homog')
            
        subs_dict = {v: v / homog_var for v in free_vars}
        f_sub = f.subs(subs_dict)
        F = sympy.expand(sympy.simplify(homog_var**d * f_sub))
        h2 = True
    except Exception:
        h2 = False
        F = None

    # ¬Q: The conclusion fails (f is irreducible iff F is irreducible is FALSE)
    try:
        def is_irreducible(poly_expr):
            if poly_expr.is_number:
                return False
            # Factor over the rationals to treat it as a polynomial over a field
            factors = sympy.factor_list(poly_expr, domain='QQ')
            # factors[1] contains the non-constant factors and their multiplicities
            if len(factors[1]) == 1 and factors[1][0][1] == 1:
                return True
            return False

        f_irred = is_irreducible(f)
        F_irred = is_irreducible(F)
        
        neg_q = (f_irred != F_irred)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-zero polynomial of degree d",
    "H_2: F is the homogenization of f",
    "¬Q: f is irreducible if and only if F is irreducible is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2