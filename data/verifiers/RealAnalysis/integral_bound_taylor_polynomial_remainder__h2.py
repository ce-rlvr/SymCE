import sympy
import math
from sympy.abc import x

def conditions(witness):
    try:
        f = witness['f']
        a = sympy.sympify(witness['a'])
        b = sympy.sympify(witness['b'])
        n = int(witness['n'])
        M = sympy.sympify(witness['M'])
        
        t_min = min(float(a), float(b))
        t_max = max(float(a), float(b))
    except Exception:
        return [False, False, False, False]

    h1 = False
    try:
        if isinstance(f, sympy.Expr):
            if t_min == t_max:
                t_vals = [t_min]
            else:
                t_vals = [t_min + i*(t_max - t_min)/10 for i in range(11)]
            
            is_real = True
            for t in t_vals:
                val = complex(f.subs(x, t).evalf())
                if abs(val.imag) > 1e-9:
                    is_real = False
                    break
            h1 = is_real
    except Exception:
        pass

    h2 = False
    try:
        if float(M) > 0:
            fn = sympy.diff(f, x, n)
            if t_min == t_max:
                t_vals = [t_min]
            else:
                t_vals = [t_min + i*(t_max - t_min)/100 for i in range(101)]
            
            bound_ok = True
            for t in t_vals:
                val_eval = fn.subs(x, t).evalf()
                c_val = complex(val_eval)
                if abs(c_val.imag) > 1e-9:
                    bound_ok = False
                    break
                if abs(c_val.real) > float(M) + 1e-7:
                    bound_ok = False
                    break
            h2 = bound_ok
    except Exception:
        pass

    h3 = False
    try:
        P = 0
        for k in range(n):
            fk = sympy.diff(f, x, k)
            fk_a = fk.subs(x, a)
            P += (fk_a / math.factorial(k)) * (x - a)**k
        h3 = True
    except Exception:
        pass

    neg_q = False
    try:
        int_f = sympy.integrate(f, (x, a, b)).evalf()
        int_P = sympy.integrate(P, (x, a, b)).evalf()
        diff_c = complex(int_f - int_P)
        lhs = abs(diff_c)
        
        rhs_expr = M / sympy.factorial(n+1) * (b - a)**(n+1)
        rhs = float(rhs_expr.evalf())
        
        if lhs > rhs + 1e-7:
            neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function on the interval",
    "H_2: There exists M > 0 bounding the nth derivative",
    "H_3: P is the Taylor polynomial of degree n-1",
    "not Q: The integral bound fails"
]

N_HYP = 3
NEG_Q_INDEX = 3