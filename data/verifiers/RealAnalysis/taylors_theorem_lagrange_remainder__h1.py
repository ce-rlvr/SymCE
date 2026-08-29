import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

x = sympy.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f^{(n+1)} exists on the open interval (a, b)",
    "¬Q: The Taylor formula equality fails for all c in (a, b)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        f, a, b, n = witness
    except Exception:
        return [False, False]
        
    try:
        f = sympy.sympify(f)
        a = float(sympy.sympify(a).evalf())
        b = float(sympy.sympify(b).evalf())
        n = int(sympy.sympify(n))
    except Exception:
        return [False, False]
        
    try:
        symbols = f.free_symbols
        x_sym = sympy.Symbol('x', real=True)
        if len(symbols) == 1:
            x_sym = list(symbols)[0]
        elif len(symbols) > 1:
            if x_sym not in symbols:
                x_sym = list(symbols)[0]
    except Exception:
        return [False, False]
        
    # Check H1: f^{(n+1)} exists on (a, b)
    h1_ok = False
    try:
        if a < b and n >= 0:
            d = sympy.diff(f, x_sym, n + 1)
            h1_ok = True
            
            try:
                sings = sympy.singularities(d, x_sym)
                if sings is not sympy.S.EmptySet:
                    for s in sings:
                        if s.is_real and a < float(s) < b:
                            h1_ok = False
                            break
            except Exception:
                pass
                
            if h1_ok:
                try:
                    d_func = sympy.lambdify(x_sym, d, modules=['math'])
                    for i in range(1, 1001):
                        val = d_func(a + i * (b - a) / 1001)
                        if isinstance(val, complex) or math.isnan(val) or math.isinf(val):
                            h1_ok = False
                            break
                except Exception:
                    for i in range(1, 101):
                        try:
                            val = d.subs(x_sym, a + i * (b - a) / 101).evalf()
                            if val.has(sympy.nan, sympy.zoo, sympy.oo, -sympy.oo) or not val.is_real:
                                h1_ok = False
                                break
                        except Exception:
                            h1_ok = False
                            break
    except Exception:
        h1_ok = False

    # Check neg_Q: Conclusion fails
    neg_q = False
    try:
        if a < b and n >= 0:
            sum_terms = 0
            undefined_terms = False
            for k in range(n + 1):
                fk = sympy.diff(f, x_sym, k)
                try:
                    fk_a = fk.subs(x_sym, a).evalf()
                    if fk_a.has(sympy.nan, sympy.zoo, sympy.oo, -sympy.oo) or not fk_a.is_real:
                        undefined_terms = True
                        break
                    sum_terms += (fk_a / sympy.factorial(k)) * (b - a)**k
                except Exception:
                    undefined_terms = True
                    break
                    
            if undefined_terms:
                neg_q = True
            else:
                try:
                    fb = f.subs(x_sym, b).evalf()
                    if fb.has(sympy.nan, sympy.zoo, sympy.oo, -sympy.oo) or not fb.is_real:
                        neg_q = True
                    else:
                        target_val = (fb - sum_terms) * sympy.factorial(n + 1) / ((b - a)**(n + 1))
                        d = sympy.diff(f, x_sym, n + 1)
                        c = sympy.Symbol('c', real=True)
                        d_c = d.subs(x_sym, c)
                        
                        found_root = False
                        
                        try:
                            sols = sympy.solve(d_c - target_val, c)
                            if isinstance(sols, list):
                                for sol in sols:
                                    try:
                                        sol_val = float(sol.evalf())
                                        if a < sol_val < b:
                                            found_root = True
                                            break
                                    except Exception:
                                        pass
                        except Exception:
                            pass
                            
                        if not found_root:
                            try:
                                diff_expr = d_c - target_val
                                diff_func = sympy.lambdify(c, diff_expr, modules=['math'])
                                prev_sign = None
                                for i in range(1, 1001):
                                    val = diff_func(a + i * (b - a) / 1001)
                                    if isinstance(val, complex) or math.isnan(val) or math.isinf(val):
                                        continue
                                    if abs(val) < 1e-7:
                                        found_root = True
                                        break
                                    sign = 1 if val > 0 else -1
                                    if prev_sign is not None and sign != prev_sign:
                                        found_root = True
                                        break
                                    prev_sign = sign
                            except Exception:
                                prev_sign = None
                                for i in range(1, 101):
                                    try:
                                        val = float((d_c - target_val).subs(c, a + i * (b - a) / 101).evalf())
                                        if abs(val) < 1e-7:
                                            found_root = True
                                            break
                                        sign = 1 if val > 0 else -1
                                        if prev_sign is not None and sign != prev_sign:
                                            found_root = True
                                            break
                                        prev_sign = sign
                                    except Exception:
                                        pass
                                        
                        neg_q = not found_root
                except Exception:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]