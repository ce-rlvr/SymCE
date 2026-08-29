import sympy
from sympy import Symbol, Poly, resultant, sqf_part

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
y = Symbol('y')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a SymPy expression in `x` representing the minimal polynomial 
    m(x) of an algebraic element \alpha over the field Q.
    """
    # Attempt to parse the witness as a polynomial over the rationals
    try:
        poly_m = Poly(witness, x, domain='QQ')
        is_poly = True
    except Exception:
        poly_m = None
        is_poly = False

    # H_1: \alpha is algebraic over F (witness is an irreducible polynomial over QQ)
    try:
        h1 = is_poly and poly_m.is_irreducible
    except Exception:
        h1 = False

    # H_2: The minimal polynomial m(x) of \alpha over F has degree n > 1
    try:
        n = poly_m.degree()
        h2 = is_poly and n > 1
    except Exception:
        n = 0
        h2 = False

    # H_3: \alpha != 1 (so m(1) != 0)
    try:
        h3 = is_poly and poly_m.eval(1) != 0
    except Exception:
        h3 = False

    # H_4: \alpha != -1 (so m(-1) != 0)
    try:
        h4 = is_poly and poly_m.eval(-1) != 0
    except Exception:
        h4 = False

    # ¬Q: The minimal polynomial of \alpha + \alpha^{-1} over F does NOT have degree n/2
    try:
        if not is_poly:
            neg_q = False
        else:
            # The minimal polynomial of \beta = \alpha + 1/\alpha divides the square-free part 
            # of the resultant of m(x) and x^2 - \beta x + 1 with respect to x.
            # Since m(x) is irreducible, the resultant is a power of the minimal polynomial of \beta.
            R = resultant(poly_m.as_expr(), x**2 - y*x + 1, x)
            R_poly = Poly(R, y, domain='QQ')
            sqf = sqf_part(R_poly.as_expr())
            deg_beta = Poly(sqf, y).degree()
            
            # The conclusion states the degree is exactly n/2. We check if it FAILS.
            neg_q = deg_beta != n / 2
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over F (witness is an irreducible polynomial over QQ)",
    "H_2: The minimal polynomial m(x) of alpha over F has degree n > 1",
    "H_3: alpha != 1",
    "H_4: alpha != -1",
    "¬Q: The minimal polynomial of alpha + alpha^{-1} over F does NOT have degree n/2"
]

N_HYP = 4
NEG_Q_INDEX = 4