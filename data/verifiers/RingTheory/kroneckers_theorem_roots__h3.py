import sympy
from sympy import Poly
from sympy.abc import x

QQ = sympy.QQ
ZZ = sympy.ZZ
GF = sympy.GF

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            F, f = witness
        else:
            F = None
            f = witness

        if isinstance(f, Poly):
            if F is None:
                F = f.domain
        else:
            try:
                f = Poly(f, x, domain=F) if F is not None else Poly(f, x)
                if F is None:
                    F = f.domain
            except Exception:
                pass

        # H1: F is a field
        try:
            if F is not None and hasattr(F, 'is_Field'):
                h1 = bool(F.is_Field)
            else:
                h1 = False
        except Exception:
            h1 = False

        # H2: f(x) is a polynomial over F
        try:
            if isinstance(f, Poly) and len(f.gens) <= 1:
                h2 = True
            else:
                h2 = False
        except Exception:
            h2 = False

        # neg_Q: f(x) has no roots in any extension field
        # This is true if and only if f(x) is a non-zero constant polynomial.
        try:
            if isinstance(f, Poly):
                if f.is_zero:
                    neg_q = False
                elif f.degree() == 0:
                    neg_q = True
                else:
                    neg_q = False
        except Exception:
            neg_q = False

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a polynomial over F",
    "not Q: f(x) has no roots in any extension field of F"
]

N_HYP = 2
NEG_Q_INDEX = 2