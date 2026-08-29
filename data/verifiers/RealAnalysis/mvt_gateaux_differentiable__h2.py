import sympy as sp

# Top-level setup for standard algebra objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        def to_tuple(obj):
            if isinstance(obj, sp.Matrix):
                return tuple(obj)
            elif isinstance(obj, (list, tuple)):
                return tuple(obj)
            else:
                return (obj,)
                
        f = witness['f']
        vars_sym = to_tuple(witness['vars'])
        x_pt = to_tuple(witness['x'])
        y_pt = to_tuple(witness['y'])
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(f, sp.Expr) and len(vars_sym) == len(x_pt) and len(vars_sym) == len(y_pt)
    except Exception:
        h1 = False
        
    try:
        t_sym = sp.Symbol('__t_dummy__', real=True)
        segment = [x_pt[i] + t_sym * (y_pt[i] - x_pt[i]) for i in range(len(vars_sym))]
        f_t = f.subs(dict(zip(vars_sym, segment)))
        df_dt = sp.diff(f_t, t_sym)
        
        h2 = True
        for i in range(11):
            val = i / 10.0
            res = df_dt.subs(t_sym, val)
            if not res.is_real:
                h2 = False
                break
    except Exception:
        h2 = False
        
    try:
        is_empty = True
        for i in range(len(x_pt)):
            if sp.simplify(x_pt[i] - y_pt[i]) != 0:
                is_empty = False
                break
                
        if is_empty:
            neg_q = True
        else:
            f_x = f.subs(dict(zip(vars_sym, x_pt)))
            f_y = f.subs(dict(zip(vars_sym, y_pt)))
            lhs = f_y - f_x
            eq = sp.simplify(df_dt - lhs)
            
            if eq == 0:
                has_sol = True
            else:
                sols = sp.solve(eq, t_sym)
                has_sol = False
                if isinstance(sols, list):
                    for sol in sols:
                        try:
                            sol_val = float(sol)
                            if 0 < sol_val < 1:
                                has_sol = True
                                break
                        except Exception:
                            if sol.is_real and (sol > 0) == True and (sol < 1) == True:
                                has_sol = True
                                break
            neg_q = not has_sol
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a topological vector space and f: X -> R",
    "H_2: f is Gateaux differentiable on an open set containing the closed line segment from x to y",
    "¬Q: There is no point c on the open line segment from x to y such that f(y) - f(x) = delta f(c; y-x)"
]

N_HYP = 2
NEG_Q_INDEX = 2