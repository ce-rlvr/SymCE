import sympy
from sympy import S, Symbol, Expr, Set, Interval, oo, limit, diff, Poly
from sympy.calculus.util import continuous_domain

x = Symbol('x')
R = S.Reals
Reals = S.Reals

def is_uniformly_continuous(expr, domain, x_sym):
    try:
        cd = continuous_domain(expr, x_sym, domain)
        if cd != domain:
            return False
    except Exception:
        pass
        
    if domain.is_bounded and domain.is_closed:
        return True
        
    if expr.is_polynomial(x_sym):
        deg = Poly(expr, x_sym).degree()
        if deg > 1 and not domain.is_bounded:
            return False
        if deg <= 1:
            return True
            
    if domain.is_Interval:
        if domain.left_open and domain.start != -oo:
            try:
                L = limit(expr, x_sym, domain.start, dir='+')
                if L in [oo, -oo]:
                    return False
            except Exception:
                pass
        if domain.right_open and domain.end != oo:
            try:
                L = limit(expr, x_sym, domain.end, dir='-')
                if L in [oo, -oo]:
                    return False
            except Exception:
                pass
                
    try:
        dexpr = diff(expr, x_sym)
        if dexpr.is_polynomial(x_sym):
            deg = Poly(dexpr, x_sym).degree()
            if deg > 0 and not domain.is_bounded:
                return False
        else:
            if domain.is_Interval and domain.end == oo:
                try:
                    L = limit(dexpr, x_sym, oo)
                    if L in [oo, -oo]:
                        return False
                except Exception:
                    pass
            if domain.is_Interval and domain.start == -oo:
                try:
                    L = limit(dexpr, x_sym, -oo)
                    if L in [oo, -oo]:
                        return False
                except Exception:
                    pass
    except Exception:
        pass
                
    raise ValueError("Cannot determine uniform continuity")

def conditions(witness):
    try:
        domain, c, f = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(domain, Set) and domain.is_subset(S.Reals)
    except Exception:
        h1 = False
        
    try:
        if isinstance(c, (int, float)):
            h2 = True
        elif hasattr(c, 'is_real') and c.is_real:
            h2 = True
        else:
            h2 = c in S.Reals
    except Exception:
        h2 = False
        
    try:
        x_sym = None
        f_expr = None
        if callable(f):
            x_sym = Symbol('x')
            f_expr = f(x_sym)
        elif isinstance(f, Expr):
            free = f.free_symbols
            if len(free) == 1:
                x_sym = list(free)[0]
                f_expr = f
            elif len(free) == 0:
                x_sym = Symbol('x')
                f_expr = f
        elif isinstance(f, (int, float)):
            x_sym = Symbol('x')
            f_expr = sympy.sympify(f)
            
        if x_sym is not None and f_expr is not None:
            g = c * f_expr
            is_uc = is_uniformly_continuous(g, domain, x_sym)
            neg_q = not is_uc
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (X, d_X) is a metric space",
    "H_2: c is a real number",
    "¬Q: g(x) = c * f(x) is not uniformly continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2