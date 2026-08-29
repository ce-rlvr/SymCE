import sympy
import math
import itertools
import functools

x = sympy.Symbol('x', real=True)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
        else:
            f, a, b = witness
            
        if float(a) >= float(b):
            return [False]
            
        integral_val = sympy.integrate(f, (x, a, b))
        lhs = float(integral_val) / float(b - a)
        
        deriv = sympy.diff(f, x)
        try:
            crit_points = sympy.solve(deriv, x)
        except Exception:
            crit_points = []
            
        max_val = float(f.subs(x, a))
        val_b = float(f.subs(x, b))
        if val_b > max_val:
            max_val = val_b
            
        if isinstance(crit_points, list):
            for cp in crit_points:
                try:
                    cp_val = float(cp)
                    if float(a) <= cp_val <= float(b):
                        val = float(f.subs(x, cp))
                        if val > max_val:
                            max_val = val
                except Exception:
                    pass
                    
        rhs = max_val / 2.0
        
        neg_q = bool(lhs < rhs)
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = ["¬Q: Average value of f is strictly less than half its maximum"]
N_HYP = 0
NEG_Q_INDEX = 0