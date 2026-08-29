import sympy as sp
import math

x, n = sp.symbols('x n', real=True)

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False
    
    if isinstance(witness, dict):
        f_expr = witness.get('f')
        a = witness.get('a')
        b = witness.get('b')
        M = witness.get('M')
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 4:
            f_expr, a, b, M = witness
        elif len(witness) == 3:
            f_expr, a, b = witness
            M = None
        else:
            return [False, False]
    else:
        return [False, False]

    if f_expr is None or a is None or b is None:
        return [False, False]

    try:
        if M is not None:
            M_val = float(M)
            if M_val > 0 and not math.isinf(M_val):
                df = sp.diff(f_expr, x)
                L = float(b) - float(a)
                if L > 0:
                    h1_ok = True
                    for n_val in [1, 2, 5, 10, 50, 100, 500, 1000]:
                        df_n = df.subs(n, n_val)
                        try:
                            df_n_lam = sp.lambdify(x, df_n, 'math')
                            use_lam = True
                        except Exception:
                            use_lam = False
                        
                        pts = [float(a) + L * (i + 0.5) / 100.0 for i in range(100)]
                        for pt in pts:
                            try:
                                val = abs(df_n_lam(pt)) if use_lam else abs(float(df_n.subs(x, pt).evalf()))
                                if val > M_val + 1e-5:
                                    h1_ok = False
                                    break
                            except Exception:
                                h1_ok = False
                                break
                        if not h1_ok:
                            break
    except Exception:
        h1_ok = False

    try:
        L = float(b) - float(a)
        if L > 0:
            delta = L / 1000.0
            max_diff = 0.0
            for n_val in [1, 2, 5, 10, 50, 100, 500, 1000]:
                f_n = f_expr.subs(n, n_val)
                try:
                    f_n_lam = sp.lambdify(x, f_n, 'math')
                    use_lam = True
                except Exception:
                    use_lam = False
                
                pts = [float(a) + L * i / 200.0 for i in range(200)]
                for x_val in pts:
                    y_val = x_val + delta
                    if y_val <= float(b):
                        try:
                            val_x = f_n_lam(x_val) if use_lam else float(f_n.subs(x, x_val).evalf())
                            val_y = f_n_lam(y_val) if use_lam else float(f_n.subs(x, y_val).evalf())
                            diff = abs(val_x - val_y)
                            if diff > max_diff:
                                max_diff = diff
                        except Exception:
                            pass
            
            if max_diff >= 0.05:
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Bounded derivative on the interval",
    "not Q: The sequence is not uniformly equicontinuous"
]

N_HYP = 1
NEG_Q_INDEX = 1