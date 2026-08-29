import sympy
from sympy import cancel, QQ, ZZ
from sympy.polys.polytools import is_irreducible
from sympy.abc import x

def conditions(witness):
    try:
        if len(witness) == 4:
            F, c, f, var = witness
        elif len(witness) == 3:
            F, c, f = witness
            var = x
        else:
            return [False, False, False, False]
            
        if callable(f):
            f_x = f(var)
            f_xc = f(var + c)
        else:
            f_x = f
            f_xc = f.subs(var, var + c)
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    try:
        h2 = bool(c in F)
    except Exception:
        h2 = False

    try:
        f_xc_simp = cancel(f_xc)
        h3 = bool(is_irreducible(f_xc_simp, domain=F))
    except Exception:
        h3 = False

    try:
        try:
            is_irred = is_irreducible(f_x, domain=F)
        except Exception:
            is_irred = False
        neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: c is an element of F",
    "H_3: The polynomial f(x+c) is irreducible over F",
    "not Q: f(x) is not irreducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3