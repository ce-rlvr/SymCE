import sympy
import math
import itertools
import functools
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False
    
    try:
        f = sympy.sympify(witness['f'])
        x_sym = witness.get('x', x)
        a = float(sympy.sympify(witness['a']).evalf())
        b = float(sympy.sympify(witness['b']).evalf())
        x_list = witness['x_list']
        
        if a < b and len(x_list) > 0:
            if f.is_polynomial(x_sym):
                h1_ok = True
            else:
                h1_ok = True
                try:
                    n, d = f.as_numer_denom()
                    if d != 1:
                        roots = sympy.solve(d, x_sym)
                        for r in roots:
                            r_eval = r.evalf()
                            if r_eval.is_real:
                                r_val = float(r_eval)
                                if a <= r_val <= b:
                                    h1_ok = False
                                    break
                except Exception:
                    pass
                
                if h1_ok:
                    for i in range(101):
                        val = a + (b - a) * i / 100.0
                        ev = f.subs(x_sym, val).evalf()
                        if not ev.is_real or not ev.is_finite:
                            h1_ok = False
                            break
    except Exception:
        h1_ok = False

    try:
        if h1_ok:
            target = sum(f.subs(x_sym, xi) for xi in x_list) / len(x_list)
            target = float(sympy.sympify(target).evalf())
            
            vals = []
            for i in range(1001):
                val = a + (b - a) * i / 1000.0
                ev = f.subs(x_sym, val).evalf()
                if ev.is_real and ev.is_finite:
                    vals.append(float(ev))
            
            try:
                df = sympy.diff(f, x_sym)
                crit_points = sympy.solve(df, x_sym)
                for cp in crit_points:
                    try:
                        cp_eval = cp.evalf()
                        if cp_eval.is_real:
                            cp_val = float(cp_eval)
                            if a <= cp_val <= b:
                                ev = f.subs(x_sym, cp_val).evalf()
                                if ev.is_real and ev.is_finite:
                                    vals.append(float(ev))
                    except Exception:
                        pass
            except Exception:
                pass
            
            if vals:
                min_val = min(vals)
                max_val = max(vals)
                
                if target < min_val - 1e-7 or target > max_val + 1e-7:
                    neg_q_ok = True
                else:
                    neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: f is continuous on the interval", "¬Q: no c exists matching the average"]

N_HYP = 1
NEG_Q_INDEX = 1