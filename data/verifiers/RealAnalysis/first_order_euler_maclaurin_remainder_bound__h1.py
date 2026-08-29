import sympy as sp
import math

x = sp.Symbol('x', real=True)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        f, n = witness
    except Exception:
        return [False, False]
        
    try:
        n_val = float(n)
        if n_val < 1:
            h1 = False
        else:
            if callable(f):
                try:
                    f = f(x)
                except Exception:
                    pass
            if not isinstance(f, sp.Expr):
                f = sp.sympify(f)
                
            df = sp.diff(f, x)
            h1 = True
            for i in range(11):
                pt = 1 + i * (n_val - 1) / 10.0
                v1 = complex(sp.N(f.subs(x, pt)))
                v2 = complex(sp.N(df.subs(x, pt)))
                if abs(v1.imag) > 1e-7 or abs(v2.imag) > 1e-7:
                    h1 = False
                    break
                if math.isnan(v1.real) or math.isnan(v2.real) or math.isinf(v1.real) or math.isinf(v2.real):
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        k_max = math.floor(n_val)
        sum_val = sum(float(sp.N(f.subs(x, k))) for k in range(1, k_max + 1))
        
        try:
            integral_val = float(sp.Integral(f, (x, 1.0, n_val)).evalf())
        except Exception:
            N_steps = 1000
            dx = (n_val - 1.0) / N_steps
            integral_val = sum(float(sp.N(f.subs(x, 1.0 + (i + 0.5) * dx))) * dx for i in range(N_steps))
        
        avg_val = (float(sp.N(f.subs(x, 1))) + float(sp.N(f.subs(x, n_val)))) / 2.0
        
        lhs = abs(sum_val - integral_val - avg_val)
        
        df_abs = sp.Abs(sp.diff(f, x))
        try:
            rhs_integral = float(sp.Integral(df_abs, (x, 1.0, n_val)).evalf())
        except Exception:
            N_steps = 1000
            dx = (n_val - 1.0) / N_steps
            rhs_integral = sum(float(sp.N(df_abs.subs(x, 1.0 + (i + 0.5) * dx))) * dx for i in range(N_steps))
            
        rhs = 0.5 * rhs_integral
        
        neg_q = lhs > rhs + 1e-7
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuously differentiable real-valued function on the closed interval from 1 to n",
    "¬Q: The Euler-Maclaurin remainder bound fails"
]

N_HYP = 1
NEG_Q_INDEX = 1