import sympy
import math
import itertools
import functools

x = sympy.Symbol('x', real=True)
n = sympy.Symbol('n', integer=True, positive=True)

def is_uniformly_convergent_to_zero(expr, x, n, a, b):
    try:
        expr_simp = sympy.simplify(expr)
        if expr_simp == 0:
            return True
        
        if not expr_simp.has(x):
            L = sympy.limit(expr_simp, n, sympy.oo)
            return L == 0
            
        max_vals = []
        for n_val in [100, 1000, 10000]:
            expr_n = expr_simp.subs(n, n_val)
            vals = []
            
            def add_val(pt):
                try:
                    val_expr = expr_n.subs(x, pt)
                    if val_expr == sympy.oo or val_expr == -sympy.oo or str(val_expr) == 'nan':
                        return False
                    val = complex(val_expr)
                    if abs(val.imag) < 1e-7:
                        vals.append(abs(val.real))
                except Exception:
                    pass
                return True

            if not add_val(a): return False
            if not add_val(b): return False
            
            try:
                crit_points = sympy.solve(sympy.diff(expr_n, x), x)
                for cp in crit_points:
                    try:
                        if cp.is_real and a <= float(cp) <= b:
                            if not add_val(float(cp)): return False
                    except Exception:
                        pass
            except Exception:
                pass
                
            try:
                points = [a + (b-a)*i/100.0 for i in range(101)]
                for i in range(1, 100):
                    points.append(a + (b-a)*i/10000.0)
                    points.append(b - (b-a)*i/10000.0)
                for p in points:
                    if not add_val(p): return False
            except Exception:
                pass
                
            if not vals:
                return False
                
            max_vals.append(max(vals))
            
        if max_vals[-1] < 1e-3:
            return True
        if max_vals[-1] < max_vals[0] * 0.2 and max_vals[-1] < 0.1:
            return True
            
        return False
    except Exception:
        return False

def check_neg_Q(a, b, f_n, g):
    try:
        for p in [a, b, (a+b)/2.0]:
            f_n_p = f_n.subs(x, p)
            L = sympy.limit(f_n_p, n, sympy.oo)
            if L == sympy.oo or L == -sympy.oo or str(L) == 'nan' or "AccumBounds" in str(L) or "Limit" in str(type(L)):
                return True
                
        f = sympy.limit(f_n, n, sympy.oo)
        if f == sympy.oo or f == -sympy.oo or str(f) == 'nan' or "AccumBounds" in str(f) or "Limit" in str(type(f)):
            return True
            
        if not is_uniformly_convergent_to_zero(f_n - f, x, n, a, b):
            return True
            
        f_prime = sympy.diff(f, x)
        diff_simp = sympy.simplify(f_prime - g)
        if diff_simp != 0:
            for p in [a, b, (a+b)/2.0]:
                val = complex(diff_simp.subs(x, p))
                if abs(val.real) > 1e-5 or abs(val.imag) > 1e-5:
                    return True
                    
        return False
    except Exception:
        try:
            vals = []
            for i in range(100, 120):
                v = complex(f_n.subs({x: a, n: i}))
                if abs(v.imag) < 1e-7:
                    vals.append(v.real)
            if max(vals) - min(vals) > 1e-2:
                return True
        except Exception:
            pass
        return False

def conditions(witness):
    try:
        a, b, f_n, g = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = float(a) < float(b)
    except Exception:
        h1 = False
        
    try:
        df = sympy.diff(f_n, x)
        h2 = True
        for p in [a, b, (a+b)/2.0]:
            v = complex(f_n.subs({x: p, n: 1}))
            if abs(v.imag) > 1e-7:
                h2 = False
                break
            val = df.subs({x: p, n: 1})
            if val == sympy.oo or val == -sympy.oo or str(val) == 'nan':
                h2 = False
                break
            cval = complex(val)
            if abs(cval.imag) > 1e-7:
                h2 = False
                break
    except Exception:
        h2 = False
        
    try:
        df = sympy.diff(f_n, x)
        h3 = is_uniformly_convergent_to_zero(df - g, x, n, a, b)
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(a, b, f_n, g)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: The interval from a to b is closed and bounded",
    "H_2: The sequence f_n consists of differentiable functions",
    "H_3: The sequence of derivatives converges uniformly to g",
    "¬Q: The sequence f_n does not converge uniformly to a differentiable function f with derivative g"
]

N_HYP = 3
NEG_Q_INDEX = 3