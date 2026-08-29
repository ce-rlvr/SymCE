import sympy as sp
from sympy import Poly, cancel, fraction, factor_list, gcd, expand, Mul, divisors
import itertools

y, x = sp.symbols('y x')

def in_R(expr, y):
    try:
        expr = expand(expr)
        if not expr.free_symbols.issubset({y}):
            return False
        poly = Poly(expr, y)
        if not poly.domain.is_ZZ:
            return False
        return poly.coeff_monomial(y) == 0
    except Exception:
        return False

def in_K(expr, y):
    try:
        if not expr.free_symbols.issubset({y}):
            return False
        n, d = fraction(cancel(expr))
        Poly(n, y, domain='ZZ')
        Poly(d, y, domain='ZZ')
        return True
    except Exception:
        return False

def get_divisors(G, y):
    coeff, factors = factor_list(G)
    int_divs = divisors(abs(coeff))
    base_divs = []
    for base, exp in factors:
        base_divs.append([base**i for i in range(exp + 1)])
    all_divs = []
    for p in itertools.product(*base_divs):
        poly_part = Mul(*p) if p else 1
        for c in int_divs:
            all_divs.append(c * poly_part)
            all_divs.append(-c * poly_part)
    return all_divs

def is_primitive(coeffs, y):
    if not coeffs or all(c == 0 for c in coeffs):
        return False
    if not all(in_R(c, y) for c in coeffs):
        return False
    G = coeffs[0]
    for c in coeffs[1:]:
        G = gcd(G, c)
    divs = get_divisors(G, y)
    for d in divs:
        if d == 1 or d == -1:
            continue
        if in_R(d, y):
            all_div = True
            for c in coeffs:
                q = cancel(c / d)
                if not in_R(q, y):
                    all_div = False
                    break
            if all_div:
                return False
    return True

def conditions(witness):
    try:
        f, g = witness
    except Exception:
        return [False, False, False]
    try:
        poly_f = Poly(f, x)
        poly_g = Poly(g, x)
        h1 = all(in_K(c, y) for c in poly_f.coeffs()) and all(in_K(c, y) for c in poly_g.coeffs())
    except Exception:
        h1 = False
    try:
        poly_f = Poly(f, x)
        h2 = is_primitive(poly_f.coeffs(), y)
    except Exception:
        h2 = False
    try:
        poly_fg = Poly(expand(f * g), x)
        fg_in_R = all(in_R(c, y) for c in poly_fg.coeffs())
        poly_g = Poly(g, x)
        g_in_R = all(in_R(c, y) for c in poly_g.coeffs())
        neg_q = fg_in_R and not g_in_R
    except Exception:
        neg_q = False
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is the fraction field of R",
    "H_2: f is a primitive polynomial",
    "not Q: intersection is not equal to ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2