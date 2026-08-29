import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: f is a primitive polynomial over R of positive degree",
    "H_3: f is irreducible over R",
    "not Q: f is reducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            expr, R = witness
            f = Poly(expr, domain=R)
        else:
            f = witness
            if not isinstance(f, Poly):
                f = Poly(f)
            R = f.domain
    except Exception:
        return [False, False, False, False]

    try:
        if hasattr(R, 'is_UFD'):
            h1 = bool(R.is_UFD)
        else:
            h1 = bool(getattr(R, 'is_Field', False) or getattr(R, 'is_PID', False) or R in (ZZ, QQ))
    except Exception:
        h1 = False

    try:
        if f.is_univariate and f.degree() > 0:
            cont = f.content()
            try:
                q = R.exquo(R.one, cont)
                is_unit = (q is not None)
            except Exception:
                is_unit = False
            h2 = is_unit
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        h3 = bool(f.is_irreducible)
    except Exception:
        h3 = False

    try:
        if hasattr(R, 'get_field'):
            F = R.get_field()
        elif hasattr(R, 'frac_field'):
            F = R.frac_field()
        else:
            F = None
        
        if F is not None:
            f_F = Poly(f.as_expr(), *f.gens, domain=F)
            neg_q = not bool(f_F.is_irreducible)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]