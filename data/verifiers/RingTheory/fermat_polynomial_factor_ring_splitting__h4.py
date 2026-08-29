import sympy
from sympy import isprime, Poly, GF, sympify
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: F_p is the finite field with p elements",
    "H_3: R is the polynomial ring over F_p",
    "not Q: R/I is not isomorphic to the direct product of p copies of F_p"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    p, I = None, None
    if isinstance(witness, dict):
        p = witness.get('p')
        I = witness.get('I')
    elif isinstance(witness, (tuple, list)) and len(witness) == 2:
        p = witness[0]
        I = witness[1]
    
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: F_p is the finite field with p elements
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: R is the polynomial ring over F_p (and I is a valid polynomial in R)
    try:
        if h1 and I is not None:
            expr_I = sympify(I)
            if expr_I.free_symbols.issubset({x}):
                # Verify it can be interpreted as a polynomial over GF(p)
                poly_I = Poly(expr_I, x, domain=GF(p))
                h3 = True
            else:
                h3 = False
        else:
            h3 = False
    except Exception:
        h3 = False

    # not Q: R/I is NOT isomorphic to F_p^p
    try:
        if not h1 or not h3:
            neg_q = False
        else:
            expr_I = sympify(I)
            poly_I = Poly(expr_I, x, domain=GF(p))
            
            # R/I is isomorphic to F_p^p iff I is a non-zero constant multiple of x^p - x
            if poly_I.is_zero:
                neg_q = True
            elif poly_I.degree() != p:
                neg_q = True
            else:
                poly_I = poly_I.monic()
                poly_target = Poly(x**p - x, x, domain=GF(p))
                neg_q = bool(poly_I != poly_target)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]