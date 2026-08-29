import sympy
from sympy import symbols, Rational, Integer, Poly, Expr
import math
import itertools
import functools

# Top-level setup
x, y, z = symbols('x y z')

def evaluate_f(f, a):
    if callable(f):
        return f(a)
    if isinstance(f, Poly):
        return f(a)
    if isinstance(f, Expr):
        free = list(f.free_symbols)
        if len(free) == 1:
            return f.subs(free[0], a)
        elif len(free) == 0:
            return f
        else:
            raise ValueError("Too many free symbols")
    if isinstance(f, (int, float)):
        return f
    raise ValueError("Cannot evaluate f")

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        F, f = witness
    except Exception:
        return [False, False, False, False]

    # H1: F is a field
    try:
        h1 = False
        if F in [sympy.QQ, sympy.RR, sympy.CC, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
            h1 = True
        elif isinstance(F, sympy.polys.domains.Field):
            h1 = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif type(F).__name__ == 'GaloisField':
            h1 = True
    except Exception:
        h1 = False

    # H2: F contains infinitely many elements
    try:
        h2 = False
        if F in [sympy.QQ, sympy.RR, sympy.CC, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
            h2 = True
        elif isinstance(F, sympy.polys.domains.CharacteristicZero):
            h2 = True
        elif hasattr(F, 'is_infinite') and F.is_infinite:
            h2 = True
        elif hasattr(F, 'order'):
            if F.order == sympy.oo:
                h2 = True
    except Exception:
        h2 = False

    # H3: For every element a in F, f(a) = 0
    try:
        h3 = True
        test_points = [0, 1, -1, 2, -2, 10, -10, Rational(1, 2), Rational(-3, 4), sympy.pi, sympy.E]
        evaluated_count = 0
        for pt in test_points:
            # Check if pt is in F
            in_F = True
            try:
                if F in [sympy.QQ, sympy.S.Rationals] or isinstance(F, sympy.polys.domains.RationalField):
                    in_F = isinstance(pt, (int, Integer, Rational))
                elif F in [sympy.RR, sympy.S.Reals] or isinstance(F, sympy.polys.domains.RealField):
                    if hasattr(pt, 'is_real'):
                        in_F = pt.is_real
            except Exception:
                pass
            
            if not in_F:
                continue
                
            try:
                val = evaluate_f(f, pt)
                evaluated_count += 1
                if sympy.simplify(val) != 0:
                    h3 = False
                    break
            except Exception:
                # If evaluation fails for a point in F, it doesn't evaluate to 0
                h3 = False
                break
        if evaluated_count == 0:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: f(x) is NOT the zero polynomial in F[x]
    try:
        if isinstance(f, (int, float)):
            is_zero = (f == 0)
        elif isinstance(f, Poly):
            is_zero = f.is_zero
        elif isinstance(f, Expr):
            if f.is_polynomial():
                is_zero = (sympy.simplify(f) == 0)
            else:
                is_zero = False
        else:
            is_zero = False
        neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: F contains infinitely many elements",
    "H_3: For every element a in F, f(a) = 0",
    "¬Q: f(x) is not the zero polynomial over F"
]

N_HYP = 3
NEG_Q_INDEX = 3