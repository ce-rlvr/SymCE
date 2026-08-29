import sympy as sp
import math

x = sp.Symbol('x', real=True)

def conditions(witness):
    try:
        if len(witness) == 4:
            f, a, b, M = witness
        elif len(witness) == 3:
            f, a, b = witness
            df = sp.diff(f, x)
            a_f = float(a)
            b_f = float(b)
            N_M = 1000
            h_M = (b_f - a_f) / N_M
            try:
                df_lam = sp.lambdify(x, df, modules=['math'])
                M = max(abs(float(df_lam(a_f + i * h_M))) for i in range(N_M + 1))
            except Exception:
                M = max(abs(float(df.subs(x, a_f + i * h_M).evalf())) for i in range(N_M + 1))
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    h1_ok = False
    try:
        if float(a) < float(b):
            df = sp.diff(f, x)
            try:
                f_lam = sp.lambdify(x, f, modules=['math'])
                df_lam = sp.lambdify(x, df, modules=['math'])
                N_pts = 100
                h_pts = float(b - a) / N_pts
                ok = True
                for i in range(N_pts + 1):
                    pt = float(a) + i * h_pts
                    v1 = float(f_lam(pt))
                    v2 = float(df_lam(pt))
                    if math.isnan(v1) or math.isinf(v1) or math.isnan(v2) or math.isinf(v2):
                        ok = False
                        break
            except Exception:
                N_pts = 20
                h_pts = float(b - a) / N_pts
                ok = True
                for i in range(N_pts + 1):
                    pt = float(a) + i * h_pts
                    v1 = float(f.subs(x, pt).evalf())
                    v2 = float(df.subs(x, pt).evalf())
                    if math.isnan(v1) or math.isinf(v1) or math.isnan(v2) or math.isinf(v2):
                        ok = False
                        break
            if ok:
                h1_ok = True
    except Exception:
        h1_ok = False
        
    neg_q_ok = False
    try:
        a_f = float(a)
        b_f = float(b)
        N = 2000
        h = (b_f - a_f) / N
        
        try:
            f_lam = sp.lambdify(x, f, modules=['math'])
            f_vals = [f_lam(a_f + i * h) for i in range(N + 1)]
        except Exception:
            f_vals = [float(f.subs(x, a_f + i * h).evalf()) for i in range(N + 1)]
            
        sum_f = f_vals[0] + f_vals[-1]
        for i in range(1, N, 2):
            sum_f += 4 * f_vals[i]
        for i in range(2, N, 2):
            sum_f += 2 * f_vals[i]
        mean_f = (h / 3.0 * sum_f) / (b_f - a_f)
        
        abs_vals = [abs(val - mean_f) for val in f_vals]
        sum_abs = abs_vals[0] + abs_vals[-1]
        for i in range(1, N, 2):
            sum_abs += 4 * abs_vals[i]
        for i in range(2, N, 2):
            sum_abs += 2 * abs_vals[i]
        lhs = h / 3.0 * sum_abs
        
        rhs = float(M) * (b_f - a_f)**2 / 4.0
        
        if lhs > rhs + 1e-5:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: f is C1", "¬Q: L1 dev > bound"]
N_HYP = 1
NEG_Q_INDEX = 1