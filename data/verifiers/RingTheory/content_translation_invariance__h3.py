import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        # Witness can be (R, f, a) or (f, a)
        if len(witness) == 3:
            R, f, a = witness
            a = sympy.sympify(a)
            if isinstance(f, Poly):
                f_expr = f.as_expr()
                poly_f = Poly(f_expr, x, domain=R)
            else:
                f_expr = sympy.sympify(f)
                poly_f = Poly(f_expr, x, domain=R)
        elif len(witness) == 2:
            f, a = witness
            a = sympy.sympify(a)
            if isinstance(f, Poly):
                f_expr = f.as_expr()
                R = f.domain
                poly_f = f
            else:
                f_expr = sympy.sympify(f)
                poly_f = Poly(f_expr, x)
                R = poly_f.domain
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    # H_2: f(x) is a polynomial over R
    try:
        if len(poly_f.gens) == 1:
            gen = poly_f.gens[0]
            h2 = True
        elif len(poly_f.gens) == 0:
            gen = x
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The content of the shifted polynomial f(x+a) does not equal the content of f(x) up to a unit.
    try:
        c1 = poly_f.content()
        f_shifted = f_expr.subs(gen, gen + a)
        poly_shifted = Poly(f_shifted, gen, domain=R)
        c2 = poly_shifted.content()
        
        if c1 == c2:
            neg_q = False
        else:
            try:
                q1 = R.exquo(c1, c2)
                q2 = R.exquo(c2, c1)
                neg_q = not (R.is_unit(q1) and R.is_unit(q2))
            except Exception:
                neg_q = True
    except Exception:
        # If f_shifted cannot be represented over R, it has no content in R,
        # so it cannot equal the content of f(x).
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f(x) is a polynomial over R",
    "¬Q: The content of f(x+a) does not equal the content of f(x) up to a unit"
]

N_HYP = 2
NEG_Q_INDEX = 2