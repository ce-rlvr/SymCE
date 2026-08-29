import sympy
from sympy import Poly, Symbol, I, Rational

x = Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            f = witness[0]
        else:
            f = witness
            
        p = Poly(f, x)
        if len(p.free_symbols) > 1:
            h1 = False
        else:
            h1 = all(c.is_rational and not getattr(c, 'is_Float', False) for c in p.coeffs())
    except Exception:
        h1 = False

    h2 = h1

    try:
        if not h1:
            neg_q = False
        else:
            p = Poly(f, x)
            roots = p.all_roots()
            neg_q = False
            for r in roots:
                if r.is_real is False:
                    neg_q = True
                    break
                try:
                    val = complex(r.evalf())
                    if abs(val.imag) > 1e-9:
                        neg_q = True
                        break
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q",
    "H_2: K is the splitting field of f(x) over Q viewed as a subfield of C",
    "not Q: K is not a subfield of the real numbers R"
]

N_HYP = 2
NEG_Q_INDEX = 2