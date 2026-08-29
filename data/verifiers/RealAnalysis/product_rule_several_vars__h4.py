import sympy
import math

x, y, z = sympy.symbols('x y z', real=True)

def conditions(witness) -> list[bool]:
    try:
        vars_tuple, f, g, a = witness
        if not isinstance(vars_tuple, (list, tuple)): return [False, False, False]
        if not all(isinstance(v, sympy.Symbol) for v in vars_tuple): return [False, False, False]
        
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        if not isinstance(f, sympy.Expr): return [False, False, False]
        if not isinstance(g, sympy.Expr): return [False, False, False]
        
        if not isinstance(a, (list, tuple)): return [False, False, False]
        if len(vars_tuple) != len(a) or len(vars_tuple) == 0: return [False, False, False]
        
        # Check if a is a point in R^n (all coordinates are real numbers)
        if not all(isinstance(val, (int, float)) or 
                   (hasattr(val, 'is_number') and val.is_number and getattr(val, 'is_real', False)) 
                   for val in a): 
            return [False, False, False]
        h1 = True
    except Exception:
        return [False, False, False]
        
    try:
        sub_dict = dict(zip(vars_tuple, a))
        f_a = f.subs(sub_dict)
        g_a = g.subs(sub_dict)
        
        # Check if f and g evaluate to finite real numbers at a
        h2 = (getattr(f_a, 'is_real', None) == True) and (getattr(g_a, 'is_real', None) == True)
        if not h2:
            try:
                v_f = float(f_a)
                v_g = float(g_a)
                if math.isfinite(v_f) and math.isfinite(v_g):
                    h2 = True
                else:
                    h2 = False
            except Exception:
                h2 = False
    except Exception:
        h2 = False
        
    try:
        def partial_deriv(expr, vars_tuple, a, i):
            v = vars_tuple[i]
            h = sympy.Symbol('__h_diff__', real=True)
            a_h = list(a)
            a_h[i] = a[i] + h
            sub_dict = dict(zip(vars_tuple, a_h))
            expr_h = expr.subs(sub_dict)
            expr_a = expr.subs(dict(zip(vars_tuple, a)))
            diff_quotient = sympy.simplify((expr_h - expr_a) / h)
            lim_plus = sympy.limit(diff_quotient, h, 0, dir='+')
            lim_minus = sympy.limit(diff_quotient, h, 0, dir='-')
            
            if lim_plus == lim_minus:
                if getattr(lim_plus, 'is_real', False) == True:
                    return lim_plus
                try:
                    v_lim = float(lim_plus)
                    if math.isfinite(v_lim):
                        return lim_plus
                except Exception:
                    pass
            return None

        fg = f * g
        conclusion_holds = True
        
        grad_fg = []
        grad_f = []
        grad_g = []
        
        for i in range(len(vars_tuple)):
            dfg = partial_deriv(fg, vars_tuple, a, i)
            df = partial_deriv(f, vars_tuple, a, i)
            dg = partial_deriv(g, vars_tuple, a, i)
            
            if dfg is None:
                conclusion_holds = False
                break
                
            grad_fg.append(dfg)
            grad_f.append(df)
            grad_g.append(dg)
            
        if conclusion_holds:
            for i in range(len(vars_tuple)):
                if grad_f[i] is None or grad_g[i] is None:
                    conclusion_holds = False
                    break
                    
                rhs = f_a * grad_g[i] + g_a * grad_f[i]
                diff = grad_fg[i] - rhs
                
                is_zero = False
                if diff == 0:
                    is_zero = True
                else:
                    try:
                        if abs(float(diff)) <= 1e-9:
                            is_zero = True
                    except Exception:
                        pass
                        
                    if not is_zero:
                        if sympy.simplify(diff) == 0:
                            is_zero = True
                            
                if not is_zero:
                    conclusion_holds = False
                    break
                    
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f and g are functions of n variables, and a is a point in R^n",
    "H_2: f and g are defined at a",
    "¬Q: fg is not differentiable at a, or its gradient is not f(a)∇g(a) + g(a)∇f(a)"
]

N_HYP = 2
NEG_Q_INDEX = 2