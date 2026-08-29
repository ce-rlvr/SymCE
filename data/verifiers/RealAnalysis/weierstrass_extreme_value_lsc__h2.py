import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: (X, d) is a compact metric space",
    "H_2: There exists at least one x in X such that f(x) < +oo",
    "¬Q: The infimum of f on X is not attained"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        X = witness.get('X')
        f_obj = witness.get('f')
        inf_val = witness.get('infimum')
        
        if X is None or f_obj is None:
            return [False, False, False]
            
        # H1: X is a compact metric space (closed bounded interval in R)
        if isinstance(X, tuple) and len(X) == 2:
            try:
                a, b = float(X[0]), float(X[1])
                h1 = (a <= b)
                X_interval = sp.Interval(a, b)
            except Exception:
                h1 = False
                X_interval = None
        elif isinstance(X, sp.Interval):
            h1 = not X.left_open and not X.right_open and X.is_bounded
            a, b = float(X.start), float(X.end)
            X_interval = X
        else:
            h1 = False
            X_interval = None
            
        if not h1 or X_interval is None:
            return [False, False, False]
            
        # Fallback for callable functions (non-SymPy)
        if not isinstance(f_obj, sp.Expr):
            if inf_val is None:
                return [bool(h1), False, False]
            inf_f = float(inf_val)
            N_dense = 100000
            dense_min = float('inf')
            for i in range(N_dense + 1):
                xv = a + i * (b - a) / N_dense
                try:
                    v = float(f_obj(xv))
                    if v < dense_min:
                        dense_min = v
                except Exception:
                    pass
            h2 = (dense_min < float('inf'))
            is_lower_bound = (dense_min >= inf_f - 1e-5)
            is_approached = (dense_min < inf_f + 1e-2)
            not_attained = (dense_min > inf_f + 1e-11)
            neg_q = is_lower_bound and is_approached and not_attained
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Rigorous SymPy path
        x_sym = witness.get('x', x)
        
        # 1. Extract critical points and discontinuities to find the true infimum
        points_to_check = {sp.sympify(a), sp.sympify(b)}
        
        def extract_points(expr):
            if isinstance(expr, sp.Piecewise):
                for e, cond in expr.args:
                    if isinstance(cond, (sp.Relational, sp.Equality, sp.Unequality)):
                        try:
                            pts = sp.solve(cond.lhs - cond.rhs, x_sym)
                            if isinstance(pts, list):
                                for p in pts:
                                    if p.is_real and a <= float(p) <= b:
                                        points_to_check.add(p)
                        except Exception:
                            pass
                    extract_points(e)
            elif isinstance(expr, sp.Expr):
                for arg in expr.args:
                    extract_points(arg)
                    
        extract_points(f_obj)
        
        try:
            deriv = sp.diff(f_obj, x_sym)
            crit_pts = sp.solve(deriv, x_sym)
            if isinstance(crit_pts, list):
                for p in crit_pts:
                    if p.is_real and a <= float(p) <= b:
                        points_to_check.add(p)
        except Exception:
            pass
            
        exact_infs = []
        for c in points_to_check:
            try:
                val = f_obj.subs(x_sym, c)
                if val.is_real or val == sp.S.NegativeInfinity:
                    exact_infs.append(val)
            except Exception:
                pass
            
            if float(c) < b:
                try:
                    lim_plus = sp.limit(f_obj, x_sym, c, dir='+')
                    if lim_plus.is_real or lim_plus == sp.S.NegativeInfinity:
                        exact_infs.append(lim_plus)
                except Exception:
                    pass
                    
            if float(c) > a:
                try:
                    lim_minus = sp.limit(f_obj, x_sym, c, dir='-')
                    if lim_minus.is_real or lim_minus == sp.S.NegativeInfinity:
                        exact_infs.append(lim_minus)
                except Exception:
                    pass
                    
        # 2. Evaluate on a grid to ensure we don't miss anything and to check H2
        N = 1000
        grid_vals = []
        for i in range(N + 1):
            xv = a + i * (b - a) / N
            try:
                val = f_obj.subs(x_sym, xv)
                if val.is_real or val == sp.S.NegativeInfinity:
                    grid_vals.append(float(val))
            except Exception:
                pass
                
        h2 = False
        for v in grid_vals:
            if v < float('inf'):
                h2 = True
                break
        if not h2:
            for v in exact_infs:
                if float(v) < float('inf'):
                    h2 = True
                    break
                    
        # 3. Determine the true infimum
        if exact_infs:
            exact_infs.sort(key=lambda val: float(val))
            best_exact_inf = exact_infs[0]
            best_inf_float = float(best_exact_inf)
        else:
            best_exact_inf = None
            best_inf_float = float('inf')
            
        if grid_vals:
            grid_min = min(grid_vals)
        else:
            grid_min = float('inf')
            
        if best_inf_float <= grid_min + 1e-5 and best_exact_inf is not None:
            inf_to_check = best_exact_inf
            inf_float = best_inf_float
        else:
            inf_to_check = grid_min
            inf_float = grid_min
            
        if inf_float == float('inf'):
            return [bool(h1), False, False]
            
        # 4. Check if the true infimum is attained
        try:
            roots = sp.solveset(sp.Eq(f_obj, inf_to_check), x_sym, domain=X_interval)
            if isinstance(roots, sp.ConditionSet):
                raise ValueError("ConditionSet returned")
            not_attained = (roots == sp.EmptySet)
        except Exception:
            # Fallback to dense grid check if solveset fails
            not_attained = True
            for v in grid_vals:
                if abs(v - inf_float) < 1e-9:
                    not_attained = False
                    break
            if not_attained:
                N_dense = 10000
                for i in range(N_dense + 1):
                    xv = a + i * (b - a) / N_dense
                    try:
                        v = float(f_obj.subs(x_sym, xv))
                        if abs(v - inf_float) < 1e-9:
                            not_attained = False
                            break
                    except Exception:
                        pass
                        
        neg_q = not_attained
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]