import sympy
from sympy.abc import x
import math

def conditions(witness):
    try:
        f, g, a, b = witness
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        a = float(a)
        b = float(b)
    except Exception:
        return [False, False, False]
        
    def check_H1():
        try:
            if a >= b:
                return False
            int_f = sympy.integrate(f, (x, a, b))
            int_g = sympy.integrate(g, (x, a, b))
            if int_f.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan):
                return False
            if int_g.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan):
                return False
            float(int_f)
            float(int_g)
            return True
        except Exception:
            return False

    def check_H2():
        try:
            if a >= b:
                return False
            n = 100
            step = (b - a) / n
            
            f_inc = True
            f_dec = True
            g_inc = True
            g_dec = True
            
            prev_f = None
            prev_g = None
            valid_points = 0
            
            for i in range(1, n):
                val = a + i * step
                try:
                    curr_f = float(f.subs(x, val))
                    curr_g = float(g.subs(x, val))
                    valid_points += 1
                except Exception:
                    continue
                    
                if prev_f is not None:
                    if curr_f < prev_f - 1e-7:
                        f_inc = False
                    if curr_f > prev_f + 1e-7:
                        f_dec = False
                if prev_g is not None:
                    if curr_g < prev_g - 1e-7:
                        g_inc = False
                    if curr_g > prev_g + 1e-7:
                        g_dec = False
                        
                prev_f = curr_f
                prev_g = curr_g
                
            if valid_points < n // 2:
                return False
                
            return (f_inc and g_inc) or (f_dec and g_dec)
        except Exception:
            return False

    def check_neg_Q():
        try:
            if a >= b:
                return True
            
            LHS_int = sympy.integrate(f * g, (x, a, b))
            if LHS_int.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan):
                return True
                
            RHS_int_f = sympy.integrate(f, (x, a, b))
            RHS_int_g = sympy.integrate(g, (x, a, b))
            
            LHS = float(LHS_int) / (b - a)
            RHS = (float(RHS_int_f) / (b - a)) * (float(RHS_int_g) / (b - a))
            
            if LHS < RHS - 1e-7:
                return True
            else:
                return False
        except Exception:
            return False

    H1_ok = check_H1()
    H2_ok = check_H2()
    neg_Q_ok = check_neg_Q()
    
    return [H1_ok, H2_ok, neg_Q_ok]

CONDITION_LABELS = ["H_1: f and g are Lebesgue integrable", "H_2: f and g are monotonic in the same direction", "¬Q: conclusion fails"]
N_HYP = 2
NEG_Q_INDEX = 2