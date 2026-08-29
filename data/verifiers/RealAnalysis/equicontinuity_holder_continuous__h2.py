import sympy
import math
import itertools
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
        
        X_pts = witness.get("X", [])
        d_func = witness.get("d")
        F_funcs = witness.get("F", [])
        M = witness.get("M")
        alpha = witness.get("alpha")
        
        if not X_pts or d_func is None or not F_funcs or M is None or alpha is None:
            return [False, False, False]
            
        if isinstance(d_func, sympy.Expr):
            syms = list(d_func.free_symbols)
            if len(syms) == 2:
                d_func = sympy.lambdify((syms[0], syms[1]), d_func, 'math')
            else:
                d_func = sympy.lambdify((x, y), d_func, 'math')
                
        F_funcs_callable = []
        for f in F_funcs:
            if isinstance(f, sympy.Expr):
                syms = list(f.free_symbols)
                if len(syms) == 1:
                    F_funcs_callable.append(sympy.lambdify(syms[0], f, 'math'))
                else:
                    F_funcs_callable.append(sympy.lambdify(x, f, 'math'))
            else:
                F_funcs_callable.append(f)
        F_funcs = F_funcs_callable
            
        h1 = True
        for p1 in X_pts:
            for p2 in X_pts:
                d12 = float(d_func(p1, p2))
                if d12 < -1e-9: h1 = False
                if p1 == p2 and abs(d12) > 1e-9: h1 = False
                if p1 != p2 and d12 < 1e-9: h1 = False
                d21 = float(d_func(p2, p1))
                if abs(d12 - d21) > 1e-9: h1 = False
                for p3 in X_pts:
                    d13 = float(d_func(p1, p3))
                    d23 = float(d_func(p2, p3))
                    if d13 > d12 + d23 + 1e-7: h1 = False
                    
        h2 = False
        if M > 0 and 0 < alpha <= 1:
            h2 = True
            for f in F_funcs:
                for p1 in X_pts:
                    for p2 in X_pts:
                        d12 = float(d_func(p1, p2))
                        diff = abs(float(f(p1)) - float(f(p2)))
                        if diff > M * (d12 ** alpha) + 1e-7:
                            h2 = False
                            
        neg_q = False
        ce_pairs = witness.get("counterexample_pairs", [])
        if ce_pairs:
            d_vals = []
            diff_vals = []
            for f, x_val, y_val in ce_pairs:
                if isinstance(f, sympy.Expr):
                    syms = list(f.free_symbols)
                    f_call = sympy.lambdify(syms[0] if syms else x, f, 'math')
                else:
                    f_call = f
                d_vals.append(float(d_func(x_val, y_val)))
                diff_vals.append(abs(float(f_call(x_val)) - float(f_call(y_val))))
            if d_vals and min(d_vals) < 1e-5 and max(diff_vals) > 1e-2:
                neg_q = True
        else:
            for f in F_funcs:
                for p1, p2 in itertools.combinations(X_pts, 2):
                    d12 = float(d_func(p1, p2))
                    if d12 < 1e-3:
                        diff = abs(float(f(p1)) - float(f(p2)))
                        if diff > 0.1:
                            neg_q = True
                            break
                if neg_q:
                    break

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: There exists M > 0 and 0 < alpha <= 1 such that for all f in F and x, y in X, |f(x) - f(y)| <= M d(x,y)^alpha",
    "not_Q: The family F is not uniformly equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2