import sympy as sp

# Top-level setup
n, x = sp.symbols('n x', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks if the given witness is a valid counterexample to the conjecture.
    The witness can be either:
      - A tuple (f_expr, limit_f, domain, n, x) where f_expr is a sympy expression.
      - A tuple (f_func, limit_f, domain, x) where f_func is a Python function f(n).
    """
    try:
        if len(witness) == 5:
            f_expr, limit_f, domain, w_n, w_x = witness
            def get_f(k):
                return f_expr.subs(w_n, k)
            # Re-bind x to the witness's x for evaluation
            eval_x = w_x
        elif len(witness) == 4:
            f_func, limit_f, domain, w_x = witness
            def get_f(k):
                return f_func(k)
            f_expr = None
            eval_x = w_x
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: {f_n} is a sequence of functions from S to R
    try:
        h1 = domain.is_subset(sp.S.Reals)
        if h1 is None:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: {f_n} converges uniformly to f on S
    h2 = False
    try:
        if len(witness) == 5 and f_expr is not None:
            diff = sp.Abs(f_expr - limit_f)
            try:
                sup = sp.calculus.util.maximum(diff, eval_x, domain)
                if sup is not sp.oo:
                    lim = sp.limit(sup, w_n, sp.oo)
                    if lim == 0:
                        h2 = True
            except Exception:
                pass
        
        if not h2:
            is_unif = True
            diff_100 = sp.Abs(get_f(100) - limit_f).simplify()
            diff_10000 = sp.Abs(get_f(10000) - limit_f).simplify()
            
            if diff_10000 != 0:
                try:
                    sup_100 = sp.calculus.util.maximum(diff_100, eval_x, domain)
                    sup_10000 = sp.calculus.util.maximum(diff_10000, eval_x, domain)
                    
                    if sup_10000 is sp.oo:
                        is_unif = False
                    elif sup_10000 > 0.1 and sup_10000 >= sup_100:
                        is_unif = False
                except Exception:
                    is_unif_points = True
                    for val_x in [0, 1, 10, 100, 1000, 1e6, -1, -10, -100, -1000, -1e6]:
                        try:
                            if domain.contains(val_x):
                                val_100 = sp.Abs(diff_100.subs(eval_x, val_x)).evalf()
                                val_10000 = sp.Abs(diff_10000.subs(eval_x, val_x)).evalf()
                                if val_10000.is_real and val_100.is_real:
                                    if val_10000 > 100:
                                        is_unif_points = False
                                        break
                                    if val_10000 > 0.1 and val_10000 >= val_100:
                                        is_unif_points = False
                                        break
                        except Exception:
                            pass
                    is_unif = is_unif_points
            h2 = is_unif
    except Exception:
        h2 = False
        
    # neg_Q: F_n does NOT converge uniformly to f on S
    neg_q = False
    try:
        for n_val in [10, 100]:
            F_n_val = sum(get_f(k) for k in range(1, n_val + 1)) / n_val
            diff_n_val = sp.Abs(F_n_val - limit_f).simplify()
            
            try:
                sup_n = sp.calculus.util.maximum(diff_n_val, eval_x, domain)
                if sup_n is sp.oo:
                    neg_q = True
                    break
            except Exception:
                pass
                
            if not neg_q:
                for val_x in [1e3, 1e6, 1e9, -1e3, -1e6, -1e9]:
                    try:
                        if domain.contains(val_x):
                            val = diff_n_val.subs(eval_x, val_x).evalf()
                            if val.is_real and val > 1e3:
                                neg_q = True
                                break
                    except Exception:
                        pass
            if neg_q:
                break
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: {f_n} is a sequence of functions from S to R",
    "H_2: The sequence {f_n} converges uniformly to f on S",
    "¬Q: The sequence of arithmetic means F_n(x) does not converge uniformly to f(x) on S"
]

N_HYP = 2
NEG_Q_INDEX = 2