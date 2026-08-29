import sympy
from sympy import Symbol, Poly, I, Rational

x = Symbol('x')

def is_radical_expr(expr):
    if expr.is_Rational:
        return True
    if expr == I:
        return True
    if expr.is_Add or expr.is_Mul:
        return all(is_radical_expr(arg) for arg in expr.args)
    if expr.is_Pow:
        base, exp = expr.args
        return is_radical_expr(base) and exp.is_Rational
    return False

def is_real_radical_expr(expr):
    try:
        c = complex(expr.evalf())
        if abs(c.imag) > 1e-9:
            return False
    except Exception:
        return False

    if expr.is_Rational:
        return True
    if expr == I:
        return False
    if expr.is_Add or expr.is_Mul:
        return all(is_real_radical_expr(arg) for arg in expr.args)
    if expr.is_Pow:
        base, exp = expr.args
        return is_real_radical_expr(base) and exp.is_Rational
    return False

def conditions(witness) -> list[bool]:
    try:
        f_raw, alpha_raw = witness
        f = sympy.sympify(f_raw)
        alpha = sympy.sympify(alpha_raw)
    except Exception:
        return [False, False, False]
    
    try:
        poly = Poly(f, x, domain='QQ')
        h1 = bool(poly.degree() == 3 and poly.is_irreducible)
    except Exception:
        h1 = False
        
    try:
        is_rad = is_radical_expr(alpha)
        val = sympy.expand(f.subs(x, alpha))
        if val == 0:
            is_root = True
        else:
            val = sympy.simplify(val)
            if val == 0:
                is_root = True
            else:
                c = complex(val.evalf())
                is_root = bool(abs(c) < 1e-9)
        h2 = bool(is_rad and is_root)
    except Exception:
        h2 = False
        
    try:
        neg_q = bool(is_real_radical_expr(alpha))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is an irreducible polynomial of degree 3 over Q",
    "H_2: K is a finite radical extension of Q containing a root of f",
    "¬Q: K is a subfield of R"
]

N_HYP = 2
NEG_Q_INDEX = 2