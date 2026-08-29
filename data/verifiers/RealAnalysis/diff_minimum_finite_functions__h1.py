import sympy

x, y, z = sympy.symbols('x y z')

def get_grad(expr, x0, vars):
    grad = []
    for i, v in enumerate(vars):
        subs_dict = {vars[k]: x0[k] for k in range(len(vars)) if k != i}
        expr_v = expr.subs(subs_dict)
        v0 = x0[i]
        
        val0 = expr_v.subs(v, v0)
        dq = (expr_v - val0) / (v - v0)
        
        try:
            right_lim = sympy.limit(dq, v, v0, dir='+')
            left_lim = sympy.limit(dq, v, v0, dir='-')
        except Exception:
            return None
            
        if type(right_lim).__name__ == 'AccumBounds' or type(left_lim).__name__ == 'AccumBounds':
            return None
            
        if right_lim.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan):
            return None
            
        diff = sympy.simplify(right_lim - left_lim)
        if diff != 0:
            try:
                if abs(float(sympy.N(diff))) > 1e-9:
                    return None
            except Exception:
                return None
                
        grad.append(right_lim)
    return grad

def conditions(witness) -> list[bool]:
    try:
        funcs, x0, vars = witness
        funcs = [sympy.sympify(f) for f in funcs]
        x0 = [sympy.sympify(v) for v in x0]
        vars = [sympy.sympify(v) for v in vars]
    except Exception:
        return [False, False, False]
        
    # H_1: f(x) = min f_i(x)
    h1_ok = True
    
    # H_2: unique minimum
    try:
        vals = [f.subs(dict(zip(vars, x0))) for f in funcs]
        vals_eval = [float(sympy.N(v)) for v in vals]
        min_val = min(vals_eval)
        
        count_min = sum(1 for v in vals_eval if abs(v - min_val) < 1e-9)
        h2_ok = (count_min == 1)
        
        if h2_ok:
            j = next(i for i, v in enumerate(vals_eval) if abs(v - min_val) < 1e-9)
        else:
            j = None
    except Exception:
        h2_ok = False
        j = None
        
    # neg_Q
    try:
        if not h2_ok or j is None:
            neg_q = False
        else:
            f_min = sympy.Min(*funcs)
            grad_f = get_grad(f_min, x0, vars)
            grad_fj = get_grad(funcs[j], x0, vars)
            
            if grad_f is None or grad_fj is None:
                neg_q = True
            else:
                neg_q = False
                for gf, gfj in zip(grad_f, grad_fj):
                    diff = sympy.simplify(gf - gfj)
                    if diff != 0:
                        try:
                            val = float(sympy.N(diff))
                            if abs(val) > 1e-9:
                                neg_q = True
                                break
                        except Exception:
                            neg_q = True
                            break
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is defined as the minimum of f_i(x)",
    "H_2: The minimum at x_0 is attained by a unique index j",
    "¬Q: f is not differentiable at x_0, or grad f(x_0) != grad f_j(x_0)"
]

N_HYP = 2
NEG_Q_INDEX = 2