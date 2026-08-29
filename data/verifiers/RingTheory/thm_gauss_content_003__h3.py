import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x, y, z

def is_unit(R, c):
    if c == R.one or c == -R.one:
        return True
    if getattr(R, 'is_Field', False) and c != R.zero:
        return True
    try:
        if c != R.zero and R.rem(R.one, c) == R.zero:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R', ZZ)
            X = witness.get('X', x)
            f_expr = witness.get('f')
            a_expr = witness.get('a')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 4:
                R, X, f_expr, a_expr = witness
            elif len(witness) == 2:
                f_expr, a_expr = witness
                R, X = ZZ, x
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    try:
        f_poly = Poly(f_expr, X, domain=R)
        cont = f_poly.content()
        h2 = is_unit(R, cont)
    except Exception:
        h2 = False

    try:
        f_poly = Poly(f_expr, X, domain=R)
        a_poly = Poly(a_expr, X, domain=R)
        g = f_poly.gcd(a_poly)
        
        if g.is_zero:
            neg_q = True
        elif g.degree() == 0:
            neg_q = not is_unit(R, g.LC())
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a primitive polynomial",
    "¬Q: The greatest common divisor of f and a is not 1"
]

N_HYP = 2
NEG_Q_INDEX = 2