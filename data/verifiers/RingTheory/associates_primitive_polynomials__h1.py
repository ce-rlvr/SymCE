import sympy
from sympy import Poly, gcd, simplify, minpoly
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if len(witness) == 3:
            f, g, var = witness
        elif len(witness) == 2:
            f, g = witness
            free = (sympy.sympify(f).free_symbols | sympy.sympify(g).free_symbols) - {sympy.I}
            var = list(free)[0] if free else sympy.Symbol('x')
        else:
            return [False, False, False]
        
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        var = sympy.sympify(var)
    except Exception:
        return [False, False, False]

    try:
        f_poly = Poly(f, var)
        g_poly = Poly(g, var)
        
        def is_algebraic_integer(val):
            try:
                dummy = sympy.Symbol('_dummy')
                p = minpoly(val, dummy)
                poly = Poly(p, dummy)
                return poly.LC() in [1, -1] and all(c.is_integer for c in poly.coeffs())
            except Exception:
                return False

        def is_unit(val):
            if val in [1, -1]:
                return True
            if val == 0:
                return False
            return is_algebraic_integer(val) and is_algebraic_integer(simplify(1/val))

        def is_primitive(poly):
            coeffs = poly.coeffs()
            if not coeffs:
                return False
            try:
                c_gcd = coeffs[0]
                for c in coeffs[1:]:
                    c_gcd = gcd(c_gcd, c)
                c_gcd = simplify(c_gcd)
                return is_unit(c_gcd)
            except Exception:
                return True

        h1 = bool(is_primitive(f_poly) and is_primitive(g_poly))
    except Exception:
        h1 = False

    try:
        LC_f = f_poly.LC()
        LC_g = g_poly.LC()
        diff = simplify(f * LC_g - g * LC_f)
        h2 = bool((diff == 0) and (f != 0) and (g != 0))
    except Exception:
        h2 = False

    try:
        u = simplify(LC_f / LC_g)
        neg_q = not is_unit(u)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f and g are primitive polynomials over R",
    "H_2: f and g are associate elements in the polynomial ring over K",
    "¬Q: f and g are not associate elements over R"
]

N_HYP = 2
NEG_Q_INDEX = 2