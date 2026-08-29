import sympy
from sympy import Symbol, Interval, S, solveset
import math

x = Symbol('x', real=True)

def evaluate_f(f, val):
    if hasattr(f, 'free_symbols'):
        symbols = list(f.free_symbols)
        if len(symbols) == 1:
            return float(f.subs(symbols[0], val))
        elif len(symbols) == 0:
            return float(f)
        else:
            return float(f.subs(x, val))
    else:
        return float(f(val))

def conditions(witness):
    try:
        if len(witness) >= 3:
            f = witness[0]
            a = witness[1]
            b = witness[2]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        val_a = evaluate_f(f, a)
        h1 = bool(val_a < 0)
    except Exception:
        h1 = False
        
    try:
        val_b = evaluate_f(f, b)
        h2 = bool(val_b > 0)
    except Exception:
        h2 = False
        
    try:
        concl_holds = None
        
        if hasattr(f, 'free_symbols'):
            try:
                symbols = list(f.free_symbols)
                var = symbols[0] if len(symbols) == 1 else x
                s = solveset(f <= 0, var, domain=Interval(a, b))
                if s != S.EmptySet and not isinstance(s, sympy.ConditionSet):
                    if hasattr(s, 'sup'):
                        c = s.sup
                        if c.is_real:
                            c_val = float(c)
                            f_c = float(f.subs(var, c_val))
                            in_interval = (float(a) < c_val < float(b))
                            is_zero = abs(f_c) < 1e-7
                            concl_holds = in_interval and is_zero
            except Exception:
                pass
                
        if concl_holds is None:
            N = 10000
            a_f = float(a)
            b_f = float(b)
            c_approx = a_f
            
            for i in range(N + 1):
                t = a_f + (b_f - a_f) * i / N
                try:
                    val = evaluate_f(f, t)
                    if val <= 0:
                        c_approx = t
                except Exception:
                    pass
                    
            step = (b_f - a_f) / N
            left = c_approx
            right = min(b_f, c_approx + step)
            
            try:
                f_right = evaluate_f(f, right)
                if f_right > 0:
                    for _ in range(50):
                        mid = (left + right) / 2.0
                        if evaluate_f(f, mid) <= 0:
                            left = mid
                        else:
                            right = mid
                    c_approx = left
            except Exception:
                pass
                
            try:
                f_c = evaluate_f(f, c_approx)
                is_zero = abs(f_c) < 1e-5
            except Exception:
                is_zero = False
                
            in_interval = (a_f < c_approx < b_f)
            if abs(c_approx - a_f) < 1e-5 or abs(c_approx - b_f) < 1e-5:
                in_interval = False
                
            concl_holds = in_interval and is_zero
            
        neg_q = not concl_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(a) < 0",
    "H_2: f(b) > 0",
    "not Q: supremum c not in (a, b) or f(c) != 0"
]
N_HYP = 2
NEG_Q_INDEX = 2