import sympy
from sympy import integrate, Abs, Interval
from sympy.calculus.util import maximum, minimum
from sympy.abc import x, y, z, t
import math

def get_var(f_sym, g_sym):
    free_syms = f_sym.free_symbols | g_sym.free_symbols
    if len(free_syms) == 1:
        return list(free_syms)[0]
    for s in free_syms:
        if s.name == 'x':
            return s
    return x

def conditions(witness):
    try:
        f, g, a, b, epsilon = witness
    except Exception:
        return [False, False]
        
    try:
        eps_ok = float(epsilon) > 0.0
        if not eps_ok:
            h1_ok = False
        elif float(a) > float(b):
            h1_ok = True
        else:
            f_sym = sympy.sympify(f)
            g_sym = sympy.sympify(g)
            diff = f_sym - g_sym
            var = get_var(f_sym, g_sym)
            
            if diff.is_constant():
                h1_ok = abs(float(diff)) <= float(epsilon)
            else:
                ivl = Interval(a, b)
                max_val = maximum(diff, var, ivl)
                min_val = minimum(diff, var, ivl)
                h1_ok = float(max_val) <= float(epsilon) and float(min_val) >= -float(epsilon)
    except Exception:
        h1_ok = False
        
    try:
        f_sym = sympy.sympify(f)
        g_sym = sympy.sympify(g)
        var = get_var(f_sym, g_sym)
        
        int_f = integrate(f_sym, (var, a, b))
        int_g = integrate(g_sym, (var, a, b))
        
        lhs = Abs(int_f - int_g)
        rhs = epsilon * (b - a)
        
        try:
            lhs_val = float(lhs)
            rhs_val = float(rhs)
            if math.isnan(lhs_val) or math.isnan(rhs_val):
                q_holds = False
            else:
                q_holds = lhs_val <= rhs_val + 1e-12
        except TypeError:
            q_holds = False
            
        neg_q_ok = not q_holds
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = ["H_1: epsilon > 0 and |f(x) - g(x)| le epsilon", "not Q: |int f - int g| > epsilon(b-a)"]

N_HYP = 1
NEG_Q_INDEX = 1