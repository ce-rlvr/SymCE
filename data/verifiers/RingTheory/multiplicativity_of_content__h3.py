import sympy
from sympy import Poly, Symbol
from sympy.abc import x, y, z
from sympy import ZZ, QQ

Z = ZZ
Q = QQ

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            f = witness.get('f')
            g = witness.get('g')
            x_var = witness.get('x', sympy.Symbol('x'))
        else:
            if len(witness) == 3:
                R, f, g = witness
                x_var = sympy.Symbol('x')
            else:
                R, f, g, x_var = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    try:
        poly_f = Poly(f, x_var, domain=R)
        h2 = not poly_f.is_zero
    except Exception:
        h2 = False

    try:
        poly_g = Poly(g, x_var, domain=R)
        poly_fg = poly_f * poly_g
        
        c_f = poly_f.content()
        c_g = poly_g.content()
        c_fg = poly_fg.content()
        
        prod = R.mul(c_f, c_g)
        
        if c_fg == prod:
            q_ok = True
        else:
            try:
                q1 = R.exquo(c_fg, prod)
                q2 = R.exquo(prod, c_fg)
                q_ok = True
            except Exception:
                q_ok = False
    except Exception:
        q_ok = False

    neg_q = not q_ok

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a non-zero polynomial over R",
    "¬Q: The content c(fg) is not associated to the product c(f)c(g) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2