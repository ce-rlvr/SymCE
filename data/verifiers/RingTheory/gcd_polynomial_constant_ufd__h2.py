import sympy
from sympy import gcd, Symbol
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: c is a non-zero element",
    "¬Q: gcd of f and c is not equal to gcd of d and c up to associates"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            c = witness.get('c')
            f = witness.get('f')
            d = witness.get('d')
        else:
            if len(witness) == 3:
                c, f, d = witness
            elif len(witness) == 4:
                _, c, f, d = witness
            else:
                return [False, False, False]
                
        c = sympy.sympify(c)
        f = sympy.sympify(f)
        d = sympy.sympify(d)
    except Exception:
        return [False, False, False]

    try:
        x_sym = Symbol('x')
        syms = f.free_symbols
        var = list(syms)[0] if syms else x_sym
        
        h1 = bool(c.is_Integer and d.is_Integer)
        if h1:
            f_poly = f.as_poly(var)
            if f_poly is None or not all(coeff.is_Integer for coeff in f_poly.coeffs()):
                h1 = False
    except Exception:
        h1 = False

    try:
        h2 = bool(c != 0)
    except Exception:
        h2 = False

    try:
        gcd_fc = gcd(f, c)
        gcd_dc = gcd(d, c)
        
        are_associates = (gcd_fc == gcd_dc) or (gcd_fc == -gcd_dc)
        neg_q = not are_associates
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]