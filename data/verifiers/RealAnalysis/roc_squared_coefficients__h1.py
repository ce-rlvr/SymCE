import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def is_zero(expr):
    try:
        if expr == 0:
            return True
        if hasattr(expr, 'is_zero_matrix') and expr.is_zero_matrix:
            return True
        if hasattr(expr, '__iter__'):
            return all(is_zero(e) for e in expr)
        if hasattr(expr, 'is_zero') and expr.is_zero:
            return True
        if hasattr(expr, 'equals'):
            return expr.equals(0)
        return False
    except Exception:
        return False

def get_R(expr, n):
    if is_zero(expr):
        return sp.oo
    
    try:
        if hasattr(expr, 'norm'):
            norm_expr = expr.norm()
        else:
            norm_expr = sp.Abs(expr)
            
        norm_expr = sp.simplify(norm_expr)
            
        if is_zero(norm_expr):
            return sp.oo
            
        L = sp.limit(norm_expr**(1/n), n, sp.oo)
        
        if isinstance(L, sp.Limit) or L.has(sp.Limit):
            return None
            
        if L == 0 or is_zero(L):
            return sp.oo
        elif L == sp.oo:
            return 0
        else:
            return 1/L
    except Exception:
        return None

def conditions(witness):
    try:
        n = sp.Symbol('n', integer=True, positive=True)
        if callable(witness):
            expr = witness(n)
        else:
            expr = witness
            
        try:
            free_symbols = getattr(expr, 'free_symbols', set())
            if free_symbols:
                for sym in free_symbols:
                    if sym.name == 'n':
                        n = sym
                        break
                else:
                    n = list(free_symbols)[0]
        except Exception:
            pass
            
        R_a = get_R(expr, n)
        R_a2 = get_R(expr**2, n)
        
        if R_a is None or R_a2 is None:
            neg_q = False
        else:
            if R_a == sp.oo:
                neg_q = (R_a2 != sp.oo)
            else:
                expected = R_a**2
                if R_a2 == sp.oo:
                    neg_q = True
                else:
                    diff = sp.simplify(R_a2 - expected)
                    neg_q = not is_zero(diff)
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: The power series sum a_n^2 x^n does not have a radius of convergence exactly equal to R^2"
]

N_HYP = 0
NEG_Q_INDEX = 0