import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference
x, y, z = sp.symbols('x y z')

def is_differentiable(expr, vars_list, a_list):
    """
    Checks if a scalar sympy expression is differentiable at a point a_list.
    """
    try:
        a_list = [sp.sympify(a_i) for a_i in a_list]
        val = expr.subs(zip(vars_list, a_list))
        if val.has(sp.oo, sp.nan, sp.zoo) or not val.is_real:
            return False
            
        grad = []
        for v in vars_list:
            h = sp.Symbol('h', real=True)
            a_v = [a_i if var != v else a_i + h for var, a_i in zip(vars_list, a_list)]
            diff_expr = (expr.subs(zip(vars_list, a_v)) - val) / h
            pd_val = sp.limit(diff_expr, h, 0)
            if pd_val.has(sp.oo, sp.nan, sp.zoo) or not pd_val.is_real:
                return False
            grad.append(pd_val)
            
        t = sp.Symbol('t', real=True, positive=True)
        h_vars = [sp.Symbol(f'h_{i}', real=True) for i in range(len(vars_list))]
        a_plus_th = [a_i + t * h_i for a_i, h_i in zip(a_list, h_vars)]
        f_a_plus_th = expr.subs(zip(vars_list, a_plus_th))
        L_h = sum(g * t * h_i for g, h_i in zip(grad, h_vars))
        
        diff = f_a_plus_th - val - L_h
        norm_h = t * sp.sqrt(sum(h_i**2 for h_i in h_vars))
        
        ratio = sp.simplify(diff / norm_h)
        if ratio == 0:
            return True
            
        lim = sp.limit(ratio, t, 0)
        if lim == 0:
            return True
            
        if isinstance(lim, sp.Expr) and lim.has(sp.Limit):
            try:
                series_exp = sp.series(ratio, t, 0, 1).removeO()
                if series_exp == 0:
                    return True
            except Exception:
                pass
                
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    witness is expected to be a dictionary with:
      - 'U_is_open': bool
      - 'f': list of sympy expressions (the component functions)
      - 'vars': list of sympy symbols
      - 'a': list of coordinates for the point
    """
    try:
        U_is_open = bool(witness.get('U_is_open', True))
    except Exception:
        U_is_open = False
        
    try:
        f_list = witness.get('f', [])
        vars_list = witness.get('vars', [])
        a_list = witness.get('a', [])
        if not isinstance(f_list, list) or not isinstance(vars_list, list) or not isinstance(a_list, list):
            H2 = False
        elif len(f_list) == 0 or len(vars_list) == 0 or len(a_list) != len(vars_list):
            H2 = False
        else:
            H2 = True
    except Exception:
        H2 = False
        
    try:
        if H2:
            all_fi_diff = True
            for f_i in f_list:
                if not is_differentiable(f_i, vars_list, a_list):
                    all_fi_diff = False
                    break
                    
            # In finite dimensions, a vector function is differentiable iff all its components are.
            f_diff = all_fi_diff
            
            # The conclusion states: f is differentiable iff each f_i is differentiable.
            # We check if this conclusion FAILS (i.e., its negation is true).
            neg_Q = not (f_diff == all_fi_diff)
        else:
            neg_Q = False
    except Exception:
        neg_Q = False
        
    return [U_is_open, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: U is an open subset of R^n",
    "H_2: f_1, ..., f_m are component functions of f",
    "¬Q: f is differentiable at a iff each f_i is differentiable at a (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2