import sympy
from sympy import Poly, QQ
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, alpha, f) or (alpha, f) where:
      - F is a sympy field domain (e.g., QQ)
      - alpha is an algebraic element
      - f is the minimal polynomial of alpha over F
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, alpha, f = witness
            elif len(witness) == 2:
                alpha, f = witness
                F = QQ
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F is a field and E/F is a field extension
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    # H_2: f(x) is the minimal polynomial of alpha over F
    try:
        if not isinstance(f, Poly):
            f_poly = Poly(f, x, domain=F)
        else:
            f_poly = f

        is_monic = (f_poly.LC() == 1)
        val = f_poly.as_expr().subs(f_poly.gen, alpha)
        is_root = (sympy.simplify(val) == 0)
        is_irred = f_poly.is_irreducible
        h2 = bool(is_monic and is_root and is_irred)
    except Exception:
        h2 = False

    # ¬Q: The minimal polynomial of alpha^-1 over F is not a_0^-1 x^n f(1/x)
    try:
        if not isinstance(f, Poly):
            f_poly = Poly(f, x, domain=F)
        else:
            f_poly = f

        a_0 = f_poly.nth(0)
        # If alpha is 0, its inverse is undefined, so the conclusion formula fails.
        if a_0 == 0 or alpha == 0:
            neg_q = True
        else:
            a_0_inv = 1 / a_0
            gen = f_poly.gen
            n = f_poly.degree()
            f_1_x = f_poly.as_expr().subs(gen, 1/gen)
            
            expected_minpoly_expr = sympy.expand(a_0_inv * (gen**n) * f_1_x)
            expected_minpoly = Poly(expected_minpoly_expr, gen, domain=F)
            
            alpha_inv = 1 / alpha
            actual_minpoly_expr = sympy.minpoly(alpha_inv, gen)
            actual_minpoly = Poly(actual_minpoly_expr, gen, domain=F)
            
            conclusion = (expected_minpoly == actual_minpoly)
            neg_q = not conclusion
    except Exception:
        # If evaluating the conclusion raises an error (e.g., ZeroDivisionError), it fails.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field and E/F is a field extension",
    "H_2: f(x) is the minimal polynomial of alpha over F",
    "¬Q: The minimal polynomial of alpha^-1 over F is not a_0^-1 x^n f(1/x)"
]

N_HYP = 2
NEG_Q_INDEX = 2