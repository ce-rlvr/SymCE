import sympy
from sympy import Symbol, limit, oo, simplify, Abs, sympify

x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    # Extract witness components
    f_n_obj = witness.get('f_n')
    f_obj = witness.get('f')
    T_obj = witness.get('T')
    
    # Convert to expressions
    if callable(f_n_obj):
        try:
            f_n_expr = f_n_obj(n, x)
        except Exception:
            try:
                f_n_expr = f_n_obj(x)
            except Exception:
                f_n_expr = f_n_obj
    else:
        f_n_expr = f_n_obj
    f_n_expr = sympify(f_n_expr)
        
    if callable(f_obj):
        try:
            f_expr = f_obj(x)
        except Exception:
            f_expr = f_obj
    else:
        f_expr = f_obj
    f_expr = sympify(f_expr)
        
    T = sympify(T_obj)
    
    # H1: T > 0 and f_n is T-periodic
    h1 = False
    try:
        is_positive = False
        try:
            is_positive = float(T) > 0
        except Exception:
            if hasattr(T, 'is_positive') and T.is_positive:
                is_positive = True
                
        if is_positive:
            diff = simplify(f_n_expr.subs(x, x + T) - f_n_expr)
            if diff == 0:
                h1 = True
            else:
                is_zero = True
                for test_n in [1, 2, 5]:
                    for test_x in [0.0, 1.5, 3.14159]:
                        try:
                            val = diff.subs({n: test_n, x: test_x}).evalf()
                            if float(Abs(val)) > 1e-7:
                                is_zero = False
                                break
                        except Exception:
                            is_zero = False
                            break
                    if not is_zero:
                        break
                h1 = is_zero
    except Exception:
        h1 = False
        
    # H2: f_n converges uniformly to f on R
    h2 = False
    try:
        # Check pointwise convergence at a few points
        is_pointwise = True
        for test_x in [0.0, 1.5, -2.1]:
            try:
                fn_val = f_n_expr.subs(x, test_x)
                f_val = f_expr.subs(x, test_x)
                lim_val = limit(fn_val, n, oo)
                if isinstance(lim_val, sympy.Limit):
                    continue
                if float(Abs((lim_val - f_val).evalf())) > 1e-7:
                    is_pointwise = False
                    break
            except Exception:
                is_pointwise = False
                break
                
        if is_pointwise:
            if 'sup_diff' in witness:
                sup_diff = witness['sup_diff']
                if callable(sup_diff):
                    try:
                        sup_diff = sup_diff(n)
                    except Exception:
                        pass
                sup_diff = sympify(sup_diff)
                lim_sup = limit(sup_diff, n, oo)
                if lim_sup == 0:
                    h2 = True
            else:
                diff = simplify(f_n_expr - f_expr)
                if x not in diff.free_symbols:
                    if limit(diff, n, oo) == 0:
                        h2 = True
                else:
                    # Check limit as n -> oo for a few x(n) to rule out non-uniform convergence
                    is_uniform = True
                    x_seqs = [n, -n, n**2, -n**2, sympy.sqrt(n), -sympy.sqrt(n), 1/n, -1/n, 1/sympy.sqrt(n), -1/sympy.sqrt(n)]
                    for x_seq in x_seqs:
                        try:
                            test_diff = diff.subs(x, x_seq)
                            lim_val = limit(test_diff, n, oo)
                            if isinstance(lim_val, sympy.Limit):
                                continue
                            if lim_val != 0:
                                is_uniform = False
                                break
                        except Exception:
                            pass
                    if is_uniform:
                        try:
                            lim_val = limit(diff, n, oo)
                            if lim_val == 0:
                                h2 = True
                        except Exception:
                            pass
    except Exception:
        h2 = False
        
    # neg_Q: f is NOT T-periodic
    neg_q = False
    try:
        diff_f = simplify(f_expr.subs(x, x + T) - f_expr)
        if diff_f != 0:
            is_zero = True
            for test_x in [0.0, 1.5, 3.14159, -2.5]:
                try:
                    val = diff_f.subs(x, test_x).evalf()
                    if float(Abs(val)) > 1e-7:
                        is_zero = False
                        break
                except Exception:
                    pass
            if not is_zero:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: There exists a real number T > 0 such that each f_n is T-periodic",
    "H_2: The sequence {f_n} converges uniformly to a function f on R",
    "¬Q: The limit function f is not T-periodic"
]

N_HYP = 2
NEG_Q_INDEX = 2