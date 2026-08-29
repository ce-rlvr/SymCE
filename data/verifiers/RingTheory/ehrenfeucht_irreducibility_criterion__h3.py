import sympy
from sympy import symbols, Poly, QQ, ZZ, GF, Rational, Integer
import math

x, y, z = symbols('x y z')

def in_K(c, K):
    try:
        res = K.from_sympy(c)
        return res is not None
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False] * 6
        K, f, g = witness
    except Exception:
        return [False] * 6

    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False

    try:
        poly_f = Poly(f, x)
        h2 = bool(all(in_K(c, K) for c in poly_f.coeffs()) and f.free_symbols.issubset({x}))
    except Exception:
        h2 = False

    try:
        deg_f = poly_f.degree()
        h3 = bool(deg_f >= 1)
    except Exception:
        h3 = False

    try:
        poly_g = Poly(g)
        deg_g = poly_g.total_degree()
        h4 = bool(deg_g >= 1)
    except Exception:
        h4 = False

    try:
        h5 = bool(math.gcd(int(deg_f), int(deg_g)) == 1)
    except Exception:
        h5 = False

    try:
        g_syms = g.free_symbols
        if len(g_syms) == 1:
            var = list(g_syms)[0]
            gy = g.subs(var, y)
        elif len(g_syms) == 0:
            gy = g
        else:
            gy = g.subs(x, y)
            
        F = f - gy
        
        if not F.free_symbols.issubset({x, y}):
            is_irred = False
        else:
            poly_F = Poly(F, x, y)
            if not all(in_K(c, K) for c in poly_F.coeffs()):
                is_irred = False
            else:
                factors = sympy.factor_list(F, domain=K)
                if len(factors[1]) == 1 and factors[1][0][1] == 1:
                    is_irred = True
                else:
                    is_irred = False
        neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = ["H_1: K is a field", "H_2: f is a polynomial over K", "H_3: deg(f) >= 1", "H_4: deg(g) >= 1", "H_5: gcd(deg(f), deg(g)) = 1", "¬Q: f(x) - g(y) is not irreducible"]

N_HYP = 5
NEG_Q_INDEX = 5