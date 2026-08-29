import sympy as sp
from sympy.abc import x

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def eval_poly(poly_expr, alpha, sym):
    poly_expr = sp.sympify(poly_expr)
    if isinstance(alpha, sp.Matrix):
        poly = sp.Poly(poly_expr, sym)
        coeffs = poly.all_coeffs()
        n = alpha.shape[0]
        res = sp.zeros(n, n)
        deg = len(coeffs) - 1
        I = sp.eye(n)
        for i in range(deg + 1):
            power = deg - i
            if power == 0:
                res += coeffs[i] * I
            else:
                res += coeffs[i] * (alpha ** power)
        return res
    else:
        return sp.simplify(poly_expr.subs(sym, alpha))

def is_zero_elem(elem):
    if isinstance(elem, sp.Matrix):
        return elem.is_zero_matrix
    else:
        return sp.simplify(elem) == 0

def is_minpoly(p, alpha, sym):
    try:
        p_poly = sp.Poly(p, sym)
        if p_poly.degree() < 1 or p_poly.LC() != 1:
            return False
        if not is_zero_elem(eval_poly(p, alpha, sym)):
            return False
        factors = sp.factor_list(p)[1]
        for base, exp in factors:
            test_p = sp.div(p, base)[0]
            if is_zero_elem(eval_poly(test_p, alpha, sym)):
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        alpha, p, g = witness
        
        h1 = isinstance(alpha, (sp.Matrix, sp.Expr, int, float))
        h2 = is_minpoly(p, alpha, x)
        
        try:
            g_poly = sp.Poly(g, x)
            h3 = True
        except Exception:
            h3 = False
            
        try:
            if h1 and h2 and h3:
                gcd_poly = sp.gcd(g, p, x)
                P = sp.Poly(gcd_poly, x).degree() == 0
                
                rem = sp.rem(g, p, x)
                Q = bool(sp.simplify(rem) != 0)
                
                neg_Q = (P != Q)
            else:
                neg_Q = False
        except Exception:
            neg_Q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: alpha is algebraic",
    "H_2: p is minpoly",
    "H_3: g is poly",
    "not_Q: equivalence fails"
]

N_HYP = 3
NEG_Q_INDEX = 3