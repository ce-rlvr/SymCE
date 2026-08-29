import sympy
import math

t = sympy.Symbol('t')
x = sympy.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
            M = witness['M']
            x_val = witness['x']
        else:
            f, a, b, M, x_val = witness
            
        if callable(f):
            t_sym = sympy.Symbol('t')
            f_expr = f(t_sym)
        else:
            f_expr = sympy.sympify(f)
            
        if len(f_expr.free_symbols) >= 1:
            if sympy.Symbol('t') in f_expr.free_symbols:
                t_sym = sympy.Symbol('t')
            elif sympy.Symbol('x') in f_expr.free_symbols:
                t_sym = sympy.Symbol('x')
            else:
                t_sym = list(f_expr.free_symbols)[0]
        else:
            t_sym = sympy.Symbol('t')
            
    except Exception:
        return [False, False]

    h1_ok = False
    try:
        a_f = float(a)
        b_f = float(b)
        if a_f < b_f:
            df = sympy.diff(f_expr, t_sym)
            h1_ok = True
            for i in range(11):
                pt = a_f + i * (b_f - a_f) / 10.0
                val_f = f_expr.subs(t_sym, pt).evalf()
                val_df = df.subs(t_sym, pt).evalf()
                if not (val_f.is_real and val_df.is_real):
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    neg_q = False
    try:
        x_f = float(x_val)
        a_f = float(a)
        b_f = float(b)
        
        if a_f <= x_f <= b_f:
            a_sym = sympy.sympify(a)
            b_sym = sympy.sympify(b)
            x_sym = sympy.sympify(x_val)
            M_sym = sympy.sympify(M)
            
            integral_val = sympy.integrate(f_expr, (t_sym, a_sym, b_sym))
            avg_val = integral_val / (b_sym - a_sym)
            
            fx = f_expr.subs(t_sym, x_sym)
            
            lhs = sympy.Abs(fx - avg_val)
            rhs = M_sym * (b_sym - a_sym) * (sympy.Rational(1, 4) + (x_sym - (a_sym + b_sym)/sympy.Rational(2))**2 / (b_sym - a_sym)**2)
            
            diff_val = (lhs - rhs).evalf()
            if diff_val > 1e-12:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = ["H_1: f is continuous and differentiable", "~Q: The Ostrowski inequality fails"]
N_HYP = 1
NEG_Q_INDEX = 1