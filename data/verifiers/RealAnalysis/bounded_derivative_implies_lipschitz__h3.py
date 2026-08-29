import sympy as sp
from sympy import Symbol, Interval, S, maximum, minimum
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

def conditions(witness):
    try:
        f, I, M = witness
    except Exception:
        return [False, False, False]
        
    # H1: I is an interval in R
    try:
        h1_ok = isinstance(I, sp.Interval) or I == S.Reals
    except Exception:
        h1_ok = False
        
    # H2: f is differentiable on I
    try:
        df = f.diff(x)
        dom_f = continuous_domain(f, x, S.Reals)
        dom_df = continuous_domain(df, x, S.Reals)
        h2_ok = bool(I.is_subset(dom_f) and I.is_subset(dom_df))
    except Exception:
        h2_ok = False
        
    # neg_Q: f is NOT Lipschitz continuous on I with Lipschitz constant M
    neg_q_ok = False
    try:
        if M < 0:
            neg_q_ok = True
        elif isinstance(I, sp.Interval) and I.start == I.end:
            neg_q_ok = False
        else:
            df = f.diff(x)
            # Try evaluating at some sample points first (fast)
            if isinstance(I, sp.Interval) or I == S.Reals:
                if I == S.Reals or (I.start == S.NegativeInfinity and I.end == S.Infinity):
                    pts = [0, 1, -1, 10, -10, 100, -100, 1000, -1000]
                elif I.start == S.NegativeInfinity:
                    e = float(I.end)
                    pts = [e-1, e-10, e-100, e-1000]
                elif I.end == S.Infinity:
                    s = float(I.start)
                    pts = [s+1, s+10, s+100, s+1000]
                else:
                    s = float(I.start)
                    e = float(I.end)
                    pts = [s + (e-s)*i/10 for i in range(1, 10)]
                    
                for p in pts:
                    try:
                        val = abs(float(df.subs(x, p)))
                        if val > M:
                            neg_q_ok = True
                            break
                    except Exception:
                        continue
                        
            if not neg_q_ok:
                try:
                    max_val = maximum(df, x, I)
                    if max_val == S.Infinity:
                        neg_q_ok = True
                    elif max_val.is_real:
                        try:
                            if float(max_val) > float(M):
                                neg_q_ok = True
                        except Exception:
                            pass
                except Exception:
                    pass
            if not neg_q_ok:
                try:
                    min_val = minimum(df, x, I)
                    if min_val == S.NegativeInfinity:
                        neg_q_ok = True
                    elif min_val.is_real:
                        try:
                            if float(min_val) < -float(M):
                                neg_q_ok = True
                        except Exception:
                            pass
                except Exception:
                    pass
    except Exception:
        pass
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I is an interval in R",
    "H_2: f is differentiable on I",
    "¬Q: f is not Lipschitz continuous on I with Lipschitz constant M"
]

N_HYP = 2
NEG_Q_INDEX = 2