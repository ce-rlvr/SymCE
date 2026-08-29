import sympy
from sympy import Symbol, Poly, degree, sympify, expand

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "The content of x^n f(1/x) is equal to the content of f(x) up to a unit."
    """
    try:
        # Extract f and n from witness
        if isinstance(witness, tuple) and len(witness) == 2:
            f, n = witness
        else:
            f = witness
            n = None
            
        # Preserve domain if witness is already a Poly
        if isinstance(f, Poly):
            p_f = f
            f_expr = p_f.as_expr()
            if n is None:
                n = p_f.degree()
        else:
            f_expr = sympify(f)
            p_f = Poly(f_expr, x)
            if n is None:
                n = degree(f_expr, x)
    except Exception:
        return [False, False, False]

    # H_1: f(x) is a non-zero polynomial in R[x]
    try:
        h1 = not p_f.is_zero
    except Exception:
        h1 = False

    # H_2: n is the degree of f(x)
    try:
        h2 = (n == p_f.degree())
    except Exception:
        h2 = False

    # Conclusion: The content of x^n f(1/x) is equal to the content of f(x) up to a unit.
    # We want neg_q to be True when they are NOT equal up to a unit.
    try:
        # Compute the reversed polynomial
        rev_expr = expand(x**n * f_expr.subs(x, 1/x))
        p_rev = Poly(rev_expr, x, domain=p_f.domain)
        
        # Compute contents
        c1 = p_f.content()
        c2 = p_rev.content()
        
        # Check if c1 and c2 are equal up to a unit
        if c1 == c2:
            q = True
        elif c1 == 0 or c2 == 0:
            q = False
        else:
            try:
                domain = p_f.domain
                d_c1 = domain.from_sympy(c1)
                d_c2 = domain.from_sympy(c2)
                # In a domain, they are equal up to a unit if they divide each other
                q = domain.divides(d_c1, d_c2) and domain.divides(d_c2, d_c1)
            except Exception:
                # Fallback if domain operations fail
                ratio = sympy.simplify(c1 / c2)
                q = (ratio == 1 or ratio == -1)
                
        neg_q = not q
    except Exception:
        # If content cannot be computed or compared (e.g., non-UFD), the conclusion fails.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a non-zero polynomial",
    "H_2: n is the degree of f(x)",
    "¬Q: The content of x^n f(1/x) is NOT equal to the content of f(x) up to a unit"
]

N_HYP = 2
NEG_Q_INDEX = 2