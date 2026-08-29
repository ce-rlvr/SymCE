import sympy
from sympy import abc

x = abc.x
Rational = sympy.Rational

def conditions(witness):
    try:
        poly = sympy.Poly(witness, x)
        n = poly.degree()
        h1 = bool(n >= 2)
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            poly_qq = sympy.Poly(witness, x, domain='QQ')
            coeffs = poly_qq.all_coeffs()
            a_n = coeffs[0]
            a_0 = coeffs[-1]
            
            factors = poly_qq.factor_list()[1]
            rational_roots = []
            for f, mult in factors:
                if f.degree() == 1:
                    coeffs_f = f.all_coeffs()
                    a, b = coeffs_f[0], coeffs_f[1]
                    root = sympy.simplify(-b / a)
                    rational_roots.append(root)
            
            h2 = True
            for r in rational_roots:
                p = sympy.Rational(r).p
                q = sympy.Rational(r).q
                
                try:
                    if q == 0:
                        q_div_an = (a_n == 0)
                    else:
                        q_div_an = sympy.Rational(sympy.simplify(a_n / q)).q == 1
                except Exception:
                    q_div_an = False
                    
                try:
                    if p == 0:
                        p_div_a0 = (a_0 == 0)
                    else:
                        p_div_a0 = sympy.Rational(sympy.simplify(a_0 / p)).q == 1
                except Exception:
                    p_div_a0 = False
                    
                if q_div_an and p_div_a0:
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        poly_qq = sympy.Poly(witness, x, domain='QQ')
        factors = poly_qq.factor_list()[1]
        has_linear_factor = any(f.degree() == 1 for f, mult in factors)
        neg_q = bool(has_linear_factor)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The degree n of f(x) is at least 2",
    "H_2: For all integers p and q with q != 0 and gcd(p, q) == 1 at least one holds: q does not divide a_n or p does not divide a_0 or f(p/q) != 0",
    "¬Q: f(x) has a linear factor over the rationals"
]

N_HYP = 2
NEG_Q_INDEX = 2