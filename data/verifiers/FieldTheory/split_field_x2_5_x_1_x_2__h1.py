import sympy
from sympy import Rational, Integer

x = sympy.Symbol('x')

CONDITION_LABELS = [
    "H_1: K is the splitting field of f(x) over Q",
    "¬Q: K is not Q(i*sqrt(5)) or degree of K over Q is not 2"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            f_expr = sympy.sympify(witness[1])
        else:
            f_expr = sympy.sympify(witness)
            
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        else:
            var = sympy.Symbol('x')
            
        poly = sympy.Poly(f_expr, var, domain='QQ')
        h1 = bool(poly.degree() >= 1)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            _, factors = sympy.factor_list(poly)
            has_deg_gt_2 = False
            has_deg_2 = False
            all_deg_2_ok = True
            
            for fac, mult in factors:
                deg = fac.degree()
                if deg > 2:
                    has_deg_gt_2 = True
                    break
                elif deg == 2:
                    has_deg_2 = True
                    coeffs = fac.all_coeffs()
                    a, b, c = coeffs[0], coeffs[1], coeffs[2]
                    disc = b**2 - 4*a*c
                    ratio = disc / -5
                    if ratio <= 0:
                        all_deg_2_ok = False
                        break
                    sq = sympy.sqrt(ratio)
                    if not sq.is_rational:
                        all_deg_2_ok = False
                        break
            
            if has_deg_gt_2 or not has_deg_2 or not all_deg_2_ok:
                is_Q_isqrt5 = False
            else:
                is_Q_isqrt5 = True
                
            neg_q = not is_Q_isqrt5
    except Exception:
        neg_q = False

    return [h1, neg_q]