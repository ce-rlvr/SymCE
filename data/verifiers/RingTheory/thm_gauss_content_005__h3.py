import sympy as sp
from sympy import Poly
from sympy.abc import x, y, z

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f and g are non-zero polynomials over R",
    "H_3: The primitive parts of f and g are associates",
    "¬Q: f and g are not associates"
]

def conditions(witness):
    try:
        f, g = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        if not isinstance(f, Poly):
            f = Poly(f)
        if not isinstance(g, Poly):
            g = Poly(g)
        f, g = f.unify(g)
    except Exception:
        return [False, False, False, False]

    # H1: R is a UFD
    try:
        domain = f.domain
        h1 = bool(getattr(domain, 'is_UFD', False))
    except Exception:
        h1 = False

    # H2: f, g are non-zero polynomials
    try:
        h2 = bool(not f.is_zero and not g.is_zero)
    except Exception:
        h2 = False

    # H3: primitive parts of f and g are associates
    try:
        c_f, pp_f = f.primitive()
        c_g, pp_g = g.primitive()
        q1, r1 = pp_f.div(pp_g)
        q2, r2 = pp_g.div(pp_f)
        h3 = bool(r1.is_zero and r2.is_zero)
    except Exception:
        h3 = False

    # neg_Q: f and g are NOT associates
    try:
        qf, rf = f.div(g)
        qg, rg = g.div(f)
        are_associates = bool(rf.is_zero and rg.is_zero)
        neg_q = not are_associates
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]