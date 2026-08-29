import sympy as sp

x, n = sp.symbols('x n')

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "¬Q: The sequence (f_n) does NOT contain a subsequence that converges uniformly on X"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        X = witness['X']
        f_n = witness['f_n']
    except Exception:
        return [False, False]
        
    # H_1: X is a compact metric space
    # We interpret X as a closed interval [a, b] in R
    h1_ok = False
    try:
        if isinstance(X, tuple) and len(X) == 2:
            a, b = X
            # Check if a and b are finite real numbers and a < b
            if (isinstance(a, (int, float)) or getattr(a, 'is_real', False)) and \
               (isinstance(b, (int, float)) or getattr(b, 'is_real', False)):
                if float(a) < float(b):
                    h1_ok = True
    except Exception:
        h1_ok = False
        
    # neg_Q: The sequence (f_n) does NOT contain a subsequence that converges uniformly on X
    neg_q_ok = False
    try:
        # To prove lack of uniformly convergent subsequence, the witness can provide
        # sequences x_n and y_n that demonstrate a failure of equicontinuity,
        # or we can check for a failure of pointwise boundedness.
        x_n = witness.get('x_n', X[0])
        y_n = witness.get('y_n', X[0])
        
        # Check if x_n and y_n are within [a, b] for large n
        valid_domain = True
        for test_n in [100, 1000, 10000]:
            try:
                xn_val = float(sp.N(x_n.subs(n, test_n) if hasattr(x_n, 'subs') else x_n))
                yn_val = float(sp.N(y_n.subs(n, test_n) if hasattr(y_n, 'subs') else y_n))
                if not (float(X[0]) - 1e-4 <= xn_val <= float(X[1]) + 1e-4):
                    valid_domain = False
                if not (float(X[0]) - 1e-4 <= yn_val <= float(X[1]) + 1e-4):
                    valid_domain = False
            except Exception:
                valid_domain = False
                break
                
        if valid_domain:
            # 1. Check equicontinuity failure
            diff_x_y = sp.limit(sp.Abs(x_n - y_n), n, sp.oo)
            
            is_diff_x_y_zero = False
            if diff_x_y == 0:
                is_diff_x_y_zero = True
            elif isinstance(diff_x_y, sp.core.expr.Expr) and diff_x_y.has(sp.Limit):
                try:
                    diff_x_y_val = float(sp.N(sp.Abs(x_n - y_n).subs(n, 100000)))
                    if diff_x_y_val < 1e-4:
                        is_diff_x_y_zero = True
                except Exception:
                    pass
            else:
                try:
                    if float(sp.N(diff_x_y)) < 1e-4:
                        is_diff_x_y_zero = True
                except Exception:
                    pass
                
            if is_diff_x_y_zero:
                val_x = f_n.subs(x, x_n) if hasattr(f_n, 'subs') else f_n
                val_y = f_n.subs(x, y_n) if hasattr(f_n, 'subs') else f_n
                diff_f = sp.limit(sp.Abs(val_x - val_y), n, sp.oo)
                
                if diff_f == sp.oo:
                    neg_q_ok = True
                elif isinstance(diff_f, sp.core.expr.Expr) and diff_f.has(sp.Limit):
                    try:
                        diff_f_val = float(sp.N(sp.Abs(val_x - val_y).subs(n, 100000)))
                        if diff_f_val > 1e-2:
                            neg_q_ok = True
                    except Exception:
                        pass
                else:
                    try:
                        if float(sp.N(diff_f)) > 0:
                            neg_q_ok = True
                    except Exception:
                        pass
            
            # 2. Check pointwise boundedness failure
            if not neg_q_ok:
                val_x = f_n.subs(x, x_n) if hasattr(f_n, 'subs') else f_n
                lim_f = sp.limit(sp.Abs(val_x), n, sp.oo)
                
                if lim_f == sp.oo:
                    neg_q_ok = True
                elif isinstance(lim_f, sp.core.expr.Expr) and lim_f.has(sp.Limit):
                    try:
                        lim_f_val = float(sp.N(sp.Abs(val_x).subs(n, 100000)))
                        if lim_f_val > 1e4:
                            neg_q_ok = True
                    except Exception:
                        pass
                else:
                    try:
                        if float(sp.N(lim_f)) > 1e4:
                            neg_q_ok = True
                    except Exception:
                        pass
                        
    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]