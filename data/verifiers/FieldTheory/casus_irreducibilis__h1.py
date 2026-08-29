import sympy
from sympy import Poly, roots, im, re, sympify
from sympy.abc import x
from sympy.polys.domains import QQ

CONDITION_LABELS = [
    "H_1: All three roots of f(x) in C are real numbers",
    "H_2: K is a finite radical extension of Q containing at least one root of f(x)",
    "¬Q: K is a subfield of the real numbers R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    witness is expected to be a tuple (f, K_gens) where:
      - f is a sympy expression in x representing the cubic polynomial
      - K_gens is a list of sympy expressions representing the generators of K over Q
    """
    try:
        f, K_gens = witness
    except Exception:
        return [False, False, False]

    # H1: f is a cubic polynomial over Q, all three roots in C are real
    h1 = False
    try:
        f_poly = Poly(f, x)
        if f_poly.degree() == 3 and all(c.is_rational for c in f_poly.coeffs()):
            rts = roots(f, x)
            if sum(rts.values()) == 3:
                h1 = all(r.is_real for r in rts.keys())
            else:
                nrts = f_poly.nroots()
                if len(nrts) == 3:
                    h1 = all(abs(im(r)) < 1e-9 for r in nrts)
    except Exception:
        h1 = False

    # H2: K is a finite radical extension of Q containing at least one root of f(x)
    h2 = False
    try:
        if isinstance(K_gens, list) and all(g.is_algebraic for g in K_gens):
            if not K_gens:
                # K = QQ
                for r in roots(f, x).keys():
                    if r.is_rational:
                        h2 = True
                        break
            else:
                # K = QQ(K_gens)
                K = QQ.algebraic_field(*K_gens)
                for r in roots(f, x).keys():
                    try:
                        K.from_expr(r)
                        h2 = True
                        break
                    except Exception:
                        pass
    except Exception:
        h2 = False

    # neg_Q: K is a subfield of R (meaning the conclusion that it is NOT a subfield fails)
    neg_q = False
    try:
        if isinstance(K_gens, list):
            neg_q = all(g.is_real for g in K_gens)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]