import sympy
from sympy import Symbol, Matrix, solveset, Interval, S, denom, cancel
import math
import itertools
import functools

x = Symbol('x', real=True)

# Top-level setup for standard algebra objects
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f, g, and h are differentiable on the open interval (a, b)",
    "H_2: a < b",
    "¬Q: For all c in (a, b), the determinant of the specified 3x3 matrix is non-zero"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_expr(func_or_expr):
    if callable(func_or_expr):
        try:
            return func_or_expr(x)
        except Exception:
            pass
    if isinstance(func_or_expr, str):
        expr = sympy.sympify(func_or_expr, locals={'x': x})
    else:
        expr = sympy.sympify(func_or_expr)
        
    free_syms = list(expr.free_symbols)
    if len(free_syms) == 1:
        sym = free_syms[0]
        if sym != x:
            expr = expr.subs(sym, x)
    else:
        for sym in free_syms:
            if sym.name == 'x' and sym != x:
                expr = expr.subs(sym, x)
    return expr

def is_diff_on_open(expr, a, b):
    from sympy.calculus.util import continuous_domain
    from sympy.calculus.singularities import singularities
    iv = Interval.open(a, b)
    try:
        dom_f = continuous_domain(expr, x, S.Reals)
        dom_df = continuous_domain(expr.diff(x), x, S.Reals)
        is_sub_f = iv.is_subset(dom_f)
        is_sub_df = iv.is_subset(dom_df)
        if is_sub_f is True and is_sub_df is True:
            return True
        if is_sub_f is False or is_sub_df is False:
            return False
    except Exception:
        pass
    
    try:
        sings_f = singularities(expr, x)
        sings_df = singularities(expr.diff(x), x)
        if sings_f.intersect(iv).is_empty is False or sings_df.intersect(iv).is_empty is False:
            return False
        if sings_f.intersect(iv).is_empty is True and sings_df.intersect(iv).is_empty is True:
            return True
    except Exception:
        pass
        
    return False

def conditions(witness):
    try:
        f, g, h, a, b = witness
    except Exception:
        return [False, False, False]
    
    try:
        f_expr = get_expr(f)
        g_expr = get_expr(g)
        h_expr = get_expr(h)
        a_val = sympy.sympify(a)
        b_val = sympy.sympify(b)
    except Exception:
        return [False, False, False]
        
    # H_1: f, g, h differentiable on (a, b)
    h1_ok = False
    try:
        h1_ok = is_diff_on_open(f_expr, a_val, b_val) and \
                is_diff_on_open(g_expr, a_val, b_val) and \
                is_diff_on_open(h_expr, a_val, b_val)
    except Exception:
        h1_ok = False
        
    # H_2: a < b
    h2_ok = False
    try:
        h2_ok = bool(a_val < b_val)
    except Exception:
        h2_ok = False
        
    # neg_Q: detM != 0 for all c in (a, b)
    neg_q_ok = False
    try:
        fa = f_expr.subs(x, a_val)
        ga = g_expr.subs(x, a_val)
        ha = h_expr.subs(x, a_val)
        
        fb = f_expr.subs(x, b_val)
        gb = g_expr.subs(x, b_val)
        hb = h_expr.subs(x, b_val)
        
        df = f_expr.diff(x)
        dg = g_expr.diff(x)
        dh = h_expr.diff(x)
        
        M = Matrix([
            [fa, ga, ha],
            [fb, gb, hb],
            [df, dg, dh]
        ])
        
        detM = M.det()
        try:
            detM_simp = cancel(detM)
        except Exception:
            detM_simp = detM
            
        iv = Interval.open(a_val, b_val)
        sols = solveset(detM_simp, x, domain=iv)
        
        if sols.is_empty is True:
            neg_q_ok = True
        elif sols.is_empty is False:
            neg_q_ok = False
        else:
            neg_q_ok = False
    except Exception:
        # If evaluation fails (e.g. nan in matrix and solveset raises error),
        # it means the determinant is undefined, so it's not zero.
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]