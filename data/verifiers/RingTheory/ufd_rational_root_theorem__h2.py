import sympy
import math

x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: f(x) is a polynomial over R",
    "H_3: p and q are elements of R",
    "H_4: p and q are coprime in R",
    "H_5: p/q is a root of f(x) in F",
    "¬Q: p does not divide a_0 or q does not divide a_n in R"
]

N_HYP = 5
NEG_Q_INDEX = 5

def divides(a, b):
    if a == 0:
        return b == 0
    try:
        if isinstance(a, int) and isinstance(b, int):
            return b % a == 0
        if getattr(a, 'is_Integer', False) and getattr(b, 'is_Integer', False):
            return int(b) % int(a) == 0
    except Exception:
        pass
    try:
        num, den = sympy.cancel(b / a).as_numer_denom()
        if den in [1, -1]:
            return True
        if hasattr(den, 'is_constant') and den.is_constant() and abs(den) == 1:
            return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        f = witness.get('f')
        p = witness.get('p')
        q = witness.get('q')
        m = witness.get('m', 0)
    except Exception:
        return [False] * 6

    h1 = True

    try:
        syms = f.free_symbols
        var = list(syms)[0] if syms else x
        f_poly = sympy.Poly(f, var)
        h2 = True
    except Exception:
        h2 = False

    try:
        p_expr = sympy.sympify(p)
        q_expr = sympy.sympify(q)
        h3 = True
    except Exception:
        h3 = False

    try:
        g = sympy.gcd(p, q)
        h4 = (g == 1 or g == -1)
    except Exception:
        h4 = False

    h5 = False
    try:
        if isinstance(p, int) and isinstance(q, int):
            frac = sympy.Rational(p, q)
        else:
            frac = p / q
        
        val = f.subs(var, frac)
        
        if m > 0:
            num, den = sympy.cancel(val).as_numer_denom()
            if num == 0:
                h5 = True
            else:
                try:
                    num_poly = sympy.Poly(num, *num.free_symbols) if num.free_symbols else sympy.Poly(num, x)
                    h5 = all(c % m == 0 for c in num_poly.coeffs())
                except Exception:
                    h5 = (int(num) % m == 0)
        else:
            h5 = sympy.simplify(val) == 0
    except Exception:
        h5 = False

    neg_q = False
    try:
        coeffs = f_poly.all_coeffs()
        a_n = coeffs[0]
        a_0 = coeffs[-1]
        div_p = divides(p, a_0)
        div_q = divides(q, a_n)
        neg_q = not (div_p and div_q)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]