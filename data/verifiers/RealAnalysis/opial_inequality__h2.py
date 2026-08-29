import sympy
import math

x = sympy.Symbol('x', real=True)

def conditions(witness):
    try:
        f, a, b = witness
        a_val = float(a)
        b_val = float(b)
        if a_val >= b_val:
            h1 = False
        else:
            df = sympy.diff(f, x)
            vals = [a_val, b_val, a_val + 0.314159*(b_val-a_val), a_val + 0.685841*(b_val-a_val)]
            h1 = True
            for v in vals:
                fv = float(f.subs(x, v).evalf())
                dfv = float(df.subs(x, v).evalf())
    except Exception:
        h1 = False

    try:
        f, a, b = witness
        a_val = float(a)
        b_val = float(b)
        df = sympy.diff(f, x)
        
        lhs_expr = sympy.Abs(f * df)
        rhs_expr = df**2
        
        def eval_integral(expr, a_v, b_v):
            try:
                res = float(sympy.Integral(expr, (x, a_v, b_v)).evalf())
                if math.isnan(res):
                    raise ValueError
                return res
            except Exception:
                f_num = sympy.lambdify(x, expr, modules=['math', 'sympy'])
                n = 1000
                dx = (b_v - a_v) / n
                val = 0.5 * float(f_num(a_v)) + 0.5 * float(f_num(b_v))
                for i in range(1, n):
                    val += float(f_num(a_v + i * dx))
                return val * dx

        lhs_val = eval_integral(lhs_expr, a_val, b_val)
        rhs_val = (b_val - a_val) / 2.0 * eval_integral(rhs_expr, a_val, b_val)
        
        neg_q = lhs_val > rhs_val + 1e-7
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuously differentiable on the interval",
    "not Q: Integral of |f*df| > (b-a)/2 * Integral of df^2"
]

N_HYP = 1
NEG_Q_INDEX = 1