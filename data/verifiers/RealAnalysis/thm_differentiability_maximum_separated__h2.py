import sympy as sp
from sympy import limit, Max
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: f(x) > g(x)",
    "¬Q: h(y) = max(f(y), g(y)) is not differentiable at x, or Dh(x) != Df(x)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        f = witness['f']
        g = witness['g']
        x_vals = witness['x']
        vars = witness['vars']
        
        if not isinstance(vars, (list, tuple)):
            vars = (vars,)
        if not isinstance(x_vals, (list, tuple)):
            x_vals = (x_vals,)
            
        subs_dict = dict(zip(vars, x_vals))
        
        f_val = f.subs(subs_dict)
        g_val = g.subs(subs_dict)
        
        # H_1: f(x) > g(x)
        try:
            h1_ok = bool(f_val > g_val)
        except Exception:
            h1_ok = False
            
        # Helper to check existence of partial derivatives
        def get_partials(expr):
            grad = []
            for var, x_val in zip(vars, x_vals):
                fixed_subs = {v: val for v, val in zip(vars, x_vals) if v != var}
                expr_1d = expr.subs(fixed_subs)
                val_1d = expr_1d.subs(var, x_val)
                
                lim_L = limit((expr_1d - val_1d)/(var - x_val), var, x_val, dir='-')
                lim_R = limit((expr_1d - val_1d)/(var - x_val), var, x_val, dir='+')
                
                if lim_L != lim_R or not lim_L.is_real:
                    return False, None
                grad.append(lim_L)
            return True, grad

        h_expr = Max(f, g)
        
        h_diff, h_grad = get_partials(h_expr)
        f_diff, f_grad = get_partials(f)
        
        # Conclusion: h is differentiable at x, and Dh(x) == Df(x)
        if not h_diff:
            q_ok = False
        elif not f_diff:
            q_ok = False
        else:
            q_ok = True
            for h_g, f_g in zip(h_grad, f_grad):
                if h_g != f_g and sp.simplify(h_g - f_g) != 0:
                    q_ok = False
                    break
            
        neg_q_ok = not q_ok
        
    except Exception:
        h1_ok = False
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]