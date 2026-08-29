import sympy
from sympy import Poly, degree

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z, t = sympy.symbols('x y z t')

def conditions(witness) -> list[bool]:
    try:
        f, g = witness
        
        # Convert to SymPy expressions if they are Poly objects or strings
        if hasattr(f, 'as_expr'):
            f = f.as_expr()
        else:
            f = sympy.sympify(f)
            
        if hasattr(g, 'as_expr'):
            g = g.as_expr()
        else:
            g = sympy.sympify(g)
    except Exception:
        return [False] * 6

    # H_1: K is a field
    try:
        poly_f = Poly(f, x)
        poly_g = Poly(g, y)
        domain = poly_f.domain.unify(poly_g.domain)
        field = domain.get_field()
        h1 = bool(field.is_Field)
    except Exception:
        h1 = False

    # H_2: f(x) in K[x]
    try:
        h2 = bool(f.is_polynomial(x)) and (y not in f.free_symbols)
    except Exception:
        h2 = False

    # H_3: g(y) in K[y]
    try:
        h3 = bool(g.is_polynomial(y)) and (x not in g.free_symbols)
    except Exception:
        h3 = False

    # H_4: deg(f) >= 1
    try:
        h4 = bool(degree(f, x) >= 1)
    except Exception:
        h4 = False

    # H_5: deg(g) >= 1
    try:
        h5 = bool(degree(g, y) >= 1)
    except Exception:
        h5 = False

    # ¬Q: f(x) - g(y) is reducible in K[x,y]
    try:
        poly_fg = Poly(f - g, x, y)
        field = poly_fg.domain.get_field()
        # Factor over the field of fractions to avoid counting constant factors as components
        poly_fg_field = Poly(f - g, x, y, domain=field)
        const, factors = poly_fg_field.factor_list()
        
        # Count the total number of non-constant factors (with multiplicity)
        num_factors = sum(power for fac, power in factors)
        neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a polynomial in x",
    "H_3: g is a polynomial in y",
    "H_4: deg(f) >= 1",
    "H_5: deg(g) >= 1",
    "¬Q: f - g is reducible"
]

N_HYP = 5
NEG_Q_INDEX = 5