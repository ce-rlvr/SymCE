import sympy as sp
from sympy.calculus.util import continuous_domain

x = sp.Symbol('x', real=True)

def conditions(witness):
    H1 = False
    H2 = False
    Neg_Q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f_expr, I_in = witness
        else:
            f_expr = witness
            I_in = sp.S.Reals
            
        if callable(f_expr):
            try:
                f_expr = f_expr(x)
            except Exception:
                pass
                
        I = None
        if I_in == sp.S.Reals:
            I = sp.Interval(-sp.oo, sp.oo)
        elif isinstance(I_in, sp.Interval):
            I = I_in
        elif isinstance(I_in, (tuple, list)) and len(I_in) == 2:
            try:
                I = sp.Interval(I_in[0], I_in[1])
            except Exception:
                pass
                
        if I is not None:
            H1 = True
            
        if H1:
            try:
                free_syms = f_expr.free_symbols
                if len(free_syms) == 1 and x not in free_syms:
                    sym = list(free_syms)[0]
                    f_expr = f_expr.subs(sym, x)
            except Exception:
                pass
                
            try:
                df = sp.diff(f_expr, x)
                dom_f = continuous_domain(f_expr, x, sp.S.Reals)
                dom_df = continuous_domain(df, x, sp.S.Reals)
                
                if I.is_subset(dom_f) and I.is_subset(dom_df):
                    H2 = True
                else:
                    H2 = False
            except Exception:
                H2 = True
                try:
                    a, b = I.start, I.end
                    a_val = float(a) if a.is_finite else None
                    b_val = float(b) if b.is_finite else None
                    
                    points = []
                    if a_val is not None and b_val is not None:
                        points = [a_val + (b_val - a_val) * i / 20.0 for i in range(0, 21)]
                    elif a_val is not None:
                        points = [a_val + i / 5.0 for i in range(0, 20)]
                    elif b_val is not None:
                        points = [b_val - i / 5.0 for i in range(0, 20)]
                    else:
                        points = [i / 5.0 for i in range(-20, 21)]
                        
                    for p in points:
                        v = df.subs(x, p)
                        if not v.is_real or abs(float(v)) == sp.oo:
                            H2 = False
                            break
                except Exception:
                    H2 = False

        if H1 and H2:
            try:
                df = sp.diff(f_expr, x)
                a, b = I.start, I.end
                a_val = float(a) if a.is_finite else None
                b_val = float(b) if b.is_finite else None
                
                # Check injectivity
                points = []
                if a_val is not None and b_val is not None:
                    points = [a_val + (b_val - a_val) * i / 10.0 for i in range(1, 10)]
                elif a_val is not None:
                    points = [a_val + i for i in range(1, 10)]
                elif b_val is not None:
                    points = [b_val - i for i in range(1, 10)]
                else:
                    points = [i for i in range(-5, 6)]
                    
                df_vals = []
                for p in points:
                    try:
                        val = float(df.subs(x, p))
                        df_vals.append(val)
                    except Exception:
                        pass
                        
                if df_vals:
                    pos = any(v > 1e-5 for v in df_vals)
                    neg = any(v < -1e-5 for v in df_vals)
                    if pos and neg:
                        Neg_Q = True
                        
                # Check uniform continuity of f^-1
                if not Neg_Q:
                    if a.is_finite and b.is_finite:
                        eps = (b - a) / 2
                    else:
                        eps = sp.Integer(1)
                        
                    g = sp.Abs(f_expr.subs(x, x + eps) - f_expr)
                    
                    endpt1 = a
                    endpt2 = b - eps if b.is_finite else sp.oo
                    
                    try:
                        if endpt1 == -sp.oo:
                            lim1 = sp.limit(g, x, endpt1)
                        else:
                            lim1 = sp.limit(g, x, endpt1, dir='+')
                        if float(lim1) == 0.0:
                            Neg_Q = True
                    except Exception:
                        pass
                        
                    if not Neg_Q:
                        try:
                            if endpt2 == sp.oo:
                                lim2 = sp.limit(g, x, endpt2)
                            else:
                                lim2 = sp.limit(g, x, endpt2, dir='-')
                            if float(lim2) == 0.0:
                                Neg_Q = True
                        except Exception:
                            pass
            except Exception:
                pass
                
    except Exception:
        pass
        
    return [H1, H2, Neg_Q]

CONDITION_LABELS = [
    "H_1: I is an interval in R",
    "H_2: f is differentiable on I",
    "¬Q: The inverse function f^-1 is NOT uniformly continuous on f(I)"
]

N_HYP = 2
NEG_Q_INDEX = 2