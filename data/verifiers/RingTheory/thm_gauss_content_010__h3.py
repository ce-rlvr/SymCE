import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import X, Y, Z

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, f, g = witness
            elif len(witness) == 2:
                f, g = witness
                R = ZZ
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        if R in (ZZ, QQ):
            h1_ok = True
        elif hasattr(R, 'is_UFD') and R.is_UFD:
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    try:
        poly_f = Poly(f, X, domain=R)
        poly_g = Poly(g, X, domain=R)
        h2_ok = not poly_f.is_zero and not poly_g.is_zero
    except Exception:
        h2_ok = False

    try:
        poly_f = Poly(f, X, domain=R)
        poly_g = Poly(g, X, domain=R)
        cf = poly_f.content()
        cg = poly_g.content()
        
        if R == ZZ:
            neg_q_ok = (cg % cf != 0)
        elif R == QQ:
            if cf == 0:
                neg_q_ok = (cg != 0)
            else:
                neg_q_ok = False
        else:
            try:
                rem = R.rem(cg, cf)
                neg_q_ok = (rem != 0)
            except Exception:
                try:
                    neg_q_ok = (cg % cf != 0)
                except Exception:
                    expr_cf = sympy.sympify(cf)
                    expr_cg = sympy.sympify(cg)
                    q, r = sympy.div(expr_cg, expr_cf)
                    neg_q_ok = (r != 0)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f and g are non-zero polynomials over R",
    "¬Q: The content of f does not divide the content of g in R"
]

N_HYP = 2
NEG_Q_INDEX = 2