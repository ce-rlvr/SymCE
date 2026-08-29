import sympy as sp
from sympy.abc import x, n
import math

def conditions(witness):
    # H_1: f_n is a sequence of real-valued functions defined on a closed and bounded interval.
    h1_ok = False
    try:
        a, b, f_n = witness
        if float(a) < float(b):
            # Check if it evaluates to a real number
            v = f_n.subs({x: a, n: 1})
            float(v)
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: The sequence f_n is uniformly equicontinuous.
    h2_ok = False
    try:
        a, b, f_n = witness
        df = sp.diff(f_n, x)
        
        def get_max_df(n_val):
            df_n = df.subs(n, n_val)
            m = 0
            try:
                if df_n.is_constant():
                    return abs(float(df_n))
            except Exception:
                pass
            
            # Evaluate on a grid to estimate the maximum absolute derivative
            for i in range(51):
                x_val = a + (b - a) * i / 50.0
                try:
                    val = abs(float(df_n.subs(x, x_val)))
                    if val > m: 
                        m = val
                except Exception:
                    pass
            return m

        m10 = get_max_df(10)
        m100 = get_max_df(100)
        
        # If the derivative grows significantly with n, it is not uniformly equicontinuous
        if m100 > m10 * 5 and m100 > m10 + 1:
            h2_ok = False
        elif m100 > 1e5:
            h2_ok = False
        else:
            h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: There exists NO subsequence of f_n that converges uniformly.
    # By Arzelà-Ascoli, an equicontinuous sequence lacks a uniformly convergent subsequence 
    # if and only if it is not pointwise bounded. We check for unboundedness.
    neg_q_ok = False
    try:
        a, b, f_n = witness
        unbounded = False
        
        for x_val in [a, b, a + (b - a) / 2.0]:
            # 1. Try exact limit
            try:
                f_x = f_n.subs(x, x_val)
                lim = sp.limit(sp.Abs(f_x), n, sp.oo)
                if lim == sp.oo:
                    unbounded = True
                    break
            except Exception:
                pass
                
            # 2. Heuristic evaluation for unbounded growth
            try:
                vals = []
                for n_val in [10, 100, 1000, 10000, 100000]:
                    vals.append(abs(float(f_n.subs({x: x_val, n: n_val}))))
                
                if max(vals) > 1e5:
                    unbounded = True
                    break
                    
                diffs = [vals[i+1] - vals[i] for i in range(len(vals)-1)]
                if all(d > 0.1 for d in diffs):
                    unbounded = True
                    break
            except Exception:
                pass
                
        neg_q_ok = unbounded
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f_n is a sequence of real functions on a closed bounded interval",
    "H_2: The sequence f_n is uniformly equicontinuous",
    "not_Q: There exists NO subsequence of f_n that converges uniformly"
]

N_HYP = 2
NEG_Q_INDEX = 2