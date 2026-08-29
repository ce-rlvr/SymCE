import sympy

x, y, z = sympy.symbols('x y z', real=True)
x1, x2, x3, x4, x5 = sympy.symbols('x1 x2 x3 x4 x5', real=True)

def conditions(witness):
    try:
        if callable(witness):
            try:
                f = witness(x)
            except Exception:
                try:
                    f = witness(x, y)
                except Exception:
                    f = witness(x, y, z)
        else:
            f = witness
            
        if not isinstance(f, sympy.Expr):
            local_dict = {'x': x, 'y': y, 'z': z, 'x1': x1, 'x2': x2, 'x3': x3, 'x4': x4, 'x5': x5}
            f = sympy.sympify(f, locals=local_dict)
            
        standard_vars = {x, y, z, x1, x2, x3, x4, x5}
        vars = sorted([v for v in f.free_symbols if v in standard_vars], key=lambda s: s.name)
        if not vars:
            vars = sorted(list(f.free_symbols), key=lambda s: s.name)
        if not vars:
            vars = [x]
            
        grad_is_2x = True
        for v in vars:
            df_dv = sympy.diff(f, v)
            diff_expr = sympy.simplify(df_dv - 2*v)
            
            is_zero = False
            if diff_expr == 0 or diff_expr is sympy.S.Zero:
                is_zero = True
            elif hasattr(diff_expr, 'is_zero') and diff_expr.is_zero:
                is_zero = True
                
            if not is_zero:
                grad_is_2x = False
                break
                
        neg_q = not grad_is_2x
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: f is not differentiable everywhere or its total derivative is not 2a·h"
]

N_HYP = 0
NEG_Q_INDEX = 0