import sympy as sp
from sympy.calculus.util import continuous_domain
from sympy import S
import math

# Top-level setup: named object bindings that the witness expression may reference
x, y, z, t, u, v, w = sp.symbols('x y z t u v w', real=True)

def check_continuity(expr):
    if not hasattr(expr, 'free_symbols'):
        return True
    symbols = list(expr.free_symbols)
    if not symbols:
        return True
    
    for sym in symbols:
        expr_1d = expr
        val = 1.1
        for other in symbols:
            if other != sym:
                expr_1d = expr_1d.subs(other, val)
                val += 1.1
        try:
            dom = continuous_domain(expr_1d, sym, S.Reals)
            if dom != S.Reals:
                return False
        except Exception:
            # Fallback if continuous_domain fails
            try:
                n, d = sp.fraction(sp.cancel(expr_1d))
                if d != 1:
                    roots = sp.solve(d, sym)
                    for r in roots:
                        if r.is_real:
                            return False
            except Exception:
                pass
                
    if len(symbols) > 1:
        sym = symbols[0]
        expr_diag = expr
        for other in symbols[1:]:
            expr_diag = expr_diag.subs(other, sym)
        try:
            dom = continuous_domain(expr_diag, sym, S.Reals)
            if dom != S.Reals:
                return False
        except Exception:
            pass
            
    return True

def is_not_uniformly_continuous(expr, sym):
    try:
        d_expr = sp.diff(expr, sym)
        
        def get_max(start, end, num_points):
            step = (end - start) / num_points
            max_val = 0
            for i in range(num_points + 1):
                val = start + i * step
                try:
                    res = d_expr.subs(sym, val).evalf()
                    if res == sp.oo or res == -sp.oo or res == sp.zoo:
                        continue
                    y = abs(float(res))
                    if y > max_val:
                        max_val = y
                except OverflowError:
                    return 'overflow'
                except Exception:
                    pass
            return max_val

        def is_growing(m1, m2, m3):
            if m3 == 'overflow':
                return True
            if m2 == 'overflow' and m1 != 'overflow':
                return True
            if m1 != 'overflow' and m2 != 'overflow':
                if m2 > 1.5 * m1 and m2 > 10:
                    return True
            if m2 != 'overflow' and m3 != 'overflow':
                if m3 > 1.2 * m2 and m3 > 10:
                    return True
            return False

        def check_positive_side():
            m1 = get_max(0, 10, 200)
            m2 = get_max(1000, 1010, 200)
            m3 = get_max(100000, 100010, 200)
            if is_growing(m1, m2, m3):
                try:
                    L = sp.limit(expr, sym, sp.oo)
                    if L.is_number and L.is_finite:
                        return False
                except Exception:
                    pass
                return True
            return False

        def check_negative_side():
            m4 = get_max(-10, 0, 200)
            m5 = get_max(-1010, -1000, 200)
            m6 = get_max(-100010, -100000, 200)
            if is_growing(m4, m5, m6):
                try:
                    L = sp.limit(expr, sym, -sp.oo)
                    if L.is_number and L.is_finite:
                        return False
                except Exception:
                    pass
                return True
            return False

        if check_positive_side():
            return True
        if check_negative_side():
            return True
            
        return False
    except Exception:
        return False

def is_not_uniformly_continuous_multivariate(expr):
    if not hasattr(expr, 'free_symbols'):
        return False
    symbols = list(expr.free_symbols)
    if not symbols:
        return False
    
    for sym in symbols:
        expr_1d = expr
        val = 0
        for other in symbols:
            if other != sym:
                expr_1d = expr_1d.subs(other, val)
        if is_not_uniformly_continuous(expr_1d, sym):
            return True
            
        expr_1d_alt = expr
        val = 1
        for other in symbols:
            if other != sym:
                expr_1d_alt = expr_1d_alt.subs(other, val)
        if is_not_uniformly_continuous(expr_1d_alt, sym):
            return True
            
    if len(symbols) > 1:
        sym = symbols[0]
        expr_diag = expr
        for other in symbols[1:]:
            expr_diag = expr_diag.subs(other, sym)
        if is_not_uniformly_continuous(expr_diag, sym):
            return True
            
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(check_continuity(witness))
    except Exception:
        h1 = False
        
    try:
        neg_q = bool(is_not_uniformly_continuous_multivariate(witness))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuous on R^n",
    "¬Q: f is not uniformly continuous on R^n"
]

N_HYP = 1
NEG_Q_INDEX = 1