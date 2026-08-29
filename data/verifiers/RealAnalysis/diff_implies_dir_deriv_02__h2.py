import sympy as sp

x, y, z = sp.symbols('x y z', real=True)

N_HYP = 4
NEG_Q_INDEX = 4

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: a is a point in U",
    "H_3: f is differentiable at a",
    "H_4: v is a vector in R^n",
    "¬Q: The directional derivative of f at a in the direction v does not exist"
]

def _has_accum_bounds(expr):
    try:
        from sympy import AccumBounds
        if isinstance(expr, AccumBounds):
            return True
        if hasattr(expr, 'has') and expr.has(AccumBounds):
            return True
    except Exception:
        pass
    return False

def _is_real_finite(expr):
    if isinstance(expr, (int, float)):
        return True
    return bool(getattr(expr, 'is_real', False) and getattr(expr, 'is_finite', False))

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            vars = witness.get('vars')
            a = witness.get('a')
            v = witness.get('v')
        else:
            f, vars, a, v = witness
    except Exception:
        return [False] * (N_HYP + 1)

    # H_1: U is an open subset of R^n
    try:
        h1_ok = isinstance(vars, (list, tuple)) and len(vars) > 0 and all(isinstance(var, sp.Symbol) for var in vars)
    except Exception:
        h1_ok = False

    # H_2: a is a point in U
    try:
        if h1_ok and isinstance(a, (list, tuple)) and len(a) == len(vars) and all(isinstance(val, (int, float, sp.Number)) for val in a):
            f_a = f.subs(zip(vars, a)).evalf()
            h2_ok = _is_real_finite(f_a)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # H_3: f is differentiable at a
    try:
        h3_ok = False
        if h2_ok:
            h = sp.Symbol('h', real=True)
            u = sp.symbols(f'u:{len(vars)}', real=True)
            f_a_exact = f.subs(zip(vars, a))
            
            grad = []
            grad_ok = True
            for i, var in enumerate(vars):
                a_plus_h = list(a)
                a_plus_h[i] = a_plus_h[i] + h
                f_eval_i = f.subs(zip(vars, a_plus_h))
                
                expr_diff = (f_eval_i - f_a_exact) / h
                df_plus = sp.limit(expr_diff, h, 0, dir='+')
                df_minus = sp.limit(expr_diff, h, 0, dir='-')
                
                if df_plus != df_minus or not _is_real_finite(df_plus) or _has_accum_bounds(df_plus):
                    grad_ok = False
                    break
                grad.append(df_plus)
            
            if grad_ok:
                a_plus_hu = [a_i + h * u_i for a_i, u_i in zip(a, u)]
                f_eval = f.subs(zip(vars, a_plus_hu))
                error = f_eval - f_a_exact - sum(g * h * u_i for g, u_i in zip(grad, u))
                
                expr_to_limit = error / h
                lim_plus = sp.limit(expr_to_limit, h, 0, dir='+')
                lim_minus = sp.limit(expr_to_limit, h, 0, dir='-')
                
                def is_zero(lim):
                    if lim == 0:
                        return True
                    try:
                        if sp.simplify(lim) == 0:
                            return True
                    except Exception:
                        pass
                    return False

                if is_zero(lim_plus) and is_zero(lim_minus):
                    h3_ok = True
    except Exception:
        h3_ok = False

    # H_4: v is a vector in R^n
    try:
        h4_ok = h1_ok and isinstance(v, (list, tuple)) and len(v) == len(vars) and all(isinstance(val, (int, float, sp.Number)) for val in v)
    except Exception:
        h4_ok = False

    # ¬Q: The directional derivative of f at a in the direction v does not exist
    try:
        neg_q_ok = False
        if h2_ok and h4_ok:
            h = sp.Symbol('h', real=True)
            f_a_exact = f.subs(zip(vars, a))
            a_plus_hv = [a_i + h * v_i for a_i, v_i in zip(a, v)]
            f_eval = f.subs(zip(vars, a_plus_hv))
            
            expr = (f_eval - f_a_exact) / h
            lim_plus = sp.limit(expr, h, 0, dir='+')
            lim_minus = sp.limit(expr, h, 0, dir='-')
            
            if lim_plus != lim_minus or not _is_real_finite(lim_plus) or _has_accum_bounds(lim_plus) or _has_accum_bounds(lim_minus):
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(h4_ok), bool(neg_q_ok)]