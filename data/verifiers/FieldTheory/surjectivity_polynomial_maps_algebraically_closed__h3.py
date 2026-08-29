import sympy

x = sympy.Symbol('x')

def conditions(witness):
    # H_1: K is an algebraically closed field
    h1 = True
    
    # H_2: f is a polynomial over K
    try:
        expr = sympy.sympify(witness)
        if not expr.free_symbols.issubset({x}):
            h2 = False
        else:
            poly_f = sympy.Poly(expr, x)
            h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: The polynomial map is NOT surjective
    try:
        expr = sympy.sympify(witness)
        poly_f = sympy.Poly(expr, x)
        # Over an algebraically closed field, a polynomial map is surjective 
        # if and only if the polynomial is non-constant.
        # Therefore, it is NOT surjective if and only if it is constant (degree <= 0).
        neg_q = bool(poly_f.degree() <= 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: f is a polynomial over K",
    "not Q: The polynomial map is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2