import sympy
from sympy import Poly, ZZ

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: R is a UFD",
    "H_2: f is non-constant",
    "H_3: f is irreducible",
    "not Q: factor ring is not an integral domain"
]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            f = witness.get('f')
            x_sym = witness.get('x')
        else:
            if len(witness) == 3:
                R, f, x_sym = witness
            elif len(witness) == 2:
                R, f = witness
                x_sym = None
            else:
                return [False, False, False, False]
                
        if x_sym is None and hasattr(f, 'free_symbols'):
            syms = list(f.free_symbols)
            if len(syms) == 1:
                x_sym = syms[0]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    try:
        poly_f = Poly(f, x_sym, domain=R)
        h2 = poly_f.degree() > 0
    except Exception:
        h2 = False

    try:
        poly_f = Poly(f, x_sym, domain=R)
        h3 = bool(poly_f.is_irreducible)
    except Exception:
        h3 = False

    try:
        poly_f = Poly(f, x_sym, domain=R)
        if poly_f.degree() <= 0:
            neg_q = False
        else:
            c = poly_f.content()
            if getattr(R, 'is_Field', False):
                is_unit = (c != 0)
            elif R == ZZ:
                is_unit = (c == 1 or c == -1)
            elif hasattr(R, 'is_unit'):
                is_unit = bool(R.is_unit(c))
            else:
                try:
                    R.exquo(R.one, c)
                    is_unit = True
                except Exception:
                    is_unit = False
            
            irred_frac = bool(poly_f.is_irreducible)
            is_integral_domain = is_unit and irred_frac
            neg_q = not is_integral_domain
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]