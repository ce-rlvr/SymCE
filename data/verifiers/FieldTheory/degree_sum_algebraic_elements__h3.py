import sympy
from sympy.abc import x

Rational = sympy.Rational
I = sympy.I
sqrt = sympy.sqrt
root = sympy.root
exp = sympy.exp
pi = sympy.pi
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        a, b = witness
    except Exception:
        return [False, False, False]
        
    try:
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        h1 = isinstance(a, sympy.Expr) and isinstance(b, sympy.Expr)
    except Exception:
        h1 = False
        
    try:
        poly_a = sympy.minpoly(a, x, domain=sympy.QQ)
        deg_a = sympy.degree(poly_a, x)
        h2 = deg_a >= 1
    except Exception:
        h2 = False
        deg_a = 0
        
    try:
        poly_b = sympy.minpoly(b, x, domain=sympy.QQ)
        poly_ab = sympy.minpoly(a + b, x, domain=sympy.QQ)
        
        deg_b = sympy.degree(poly_b, x)
        deg_ab = sympy.degree(poly_ab, x)
        
        if deg_ab == 0:
            neg_q = False
        else:
            neg_q = (deg_a * deg_b) % deg_ab != 0
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L over K is a field extension",
    "H_2: a is an element of L that is algebraic over K",
    "not Q: The degree of K(a+b) over K does not divide the product of degrees"
]

N_HYP = 2
NEG_Q_INDEX = 2