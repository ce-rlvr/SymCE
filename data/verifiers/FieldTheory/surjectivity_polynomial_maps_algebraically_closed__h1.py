import sympy
from sympy import Poly
from sympy.abc import x

# Top-level setup for potential witness expressions
Z2 = sympy.polys.domains.GF(2)
Z3 = sympy.polys.domains.GF(3)
Z5 = sympy.polys.domains.GF(5)
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    # Parse the witness into a sympy Poly object
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            expr, domain = witness
            f = Poly(expr, x, domain=domain)
        elif isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness, x, domain='QQ')
        
        # H1: f is a polynomial over a field K
        if hasattr(f.domain, 'is_Field') and f.domain.is_Field:
            h1 = f.is_univariate
        elif f.domain in (sympy.QQ, sympy.RR, sympy.CC):
            h1 = f.is_univariate
        elif getattr(f.domain, 'is_FiniteField', False):
            h1 = f.is_univariate
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: f is non-constant
    try:
        if h1:
            h2 = f.degree() > 0
    except Exception:
        h2 = False

    # ¬Q: The polynomial map c |-> f(c) is NOT surjective from K onto K
    try:
        if h1 and h2:
            if getattr(f.domain, 'is_FiniteField', False):
                p = f.domain.order
                image = set()
                expr = f.as_expr()
                for i in range(p):
                    val = expr.subs(x, i)
                    image.add(int(val) % p)
                neg_q = len(image) < p
                
            elif f.domain == sympy.QQ:
                found_missing = False
                expr = f.as_expr()
                # Search for a value y in Q that has no pre-image
                for y in range(-100, 101):
                    shifted = expr - y
                    rts = sympy.roots(shifted, x, domain='QQ')
                    if not rts:  # No rational roots found
                        found_missing = True
                        break
                neg_q = found_missing
                
            elif f.domain == sympy.RR:
                # Over R, polynomials are surjective iff their degree is odd
                neg_q = (f.degree() % 2 == 0)
                
            elif f.domain == sympy.CC:
                # Over C, all non-constant polynomials are surjective
                neg_q = False
                
            else:
                # Fallback for other fields
                found_missing = False
                expr = f.as_expr()
                for y in range(-100, 101):
                    shifted = expr - y
                    rts = sympy.roots(shifted, x)
                    if not rts:
                        found_missing = True
                        break
                neg_q = found_missing
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over a field K",
    "H_2: f is non-constant",
    "¬Q: The polynomial map c |-> f(c) is NOT surjective from K onto K"
]

N_HYP = 2
NEG_Q_INDEX = 2