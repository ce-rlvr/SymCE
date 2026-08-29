import sympy as sp
import math

# Top-level setup
x, n = sp.symbols('x n')

def check_h1(witness):
    try:
        X, f_n = witness
        if not isinstance(X, sp.Interval):
            return False
        return (not X.left_open) and (not X.right_open) and X.start.is_finite and X.end.is_finite
    except Exception:
        return False

def check_h2(witness):
    # Y is implicitly R (since we use real-valued SymPy expressions), which is complete
    return True

def check_h3(witness):
    try:
        X, f_n = witness
        for n_val in [1, 2, 5]:
            f_n_expr = f_n.subs(n, n_val)
            try:
                dom = sp.calculus.util.continuous_domain(f_n_expr, x, sp.S.Reals)
                if not X.is_subset(dom):
                    return False
            except Exception:
                try:
                    sings = sp.calculus.singularities.singularities(f_n_expr, x)
                    if sings.intersect(X) != sp.EmptySet:
                        return False
                except Exception:
                    pass
        return True
    except Exception:
        return False

def check_h4(witness):
    try:
        X, f_n = witness
        start = float(X.start)
        end = float(X.end)
        N_grid = 50
        grid = [start + i * (end - start) / N_grid for i in range(N_grid + 1)]
        for pt in grid:
            try:
                L = sp.limit(f_n.subs(x, pt), n, sp.oo)
                if not L.is_number or not L.is_finite or not L.is_real:
                    val1 = float(f_n.subs({n: 1000, x: pt}))
                    val2 = float(f_n.subs({n: 2000, x: pt}))
                    val3 = float(f_n.subs({n: 3000, x: pt}))
                    if abs(val1 - val2) > 1e-2 or abs(val2 - val3) > 1e-2:
                        return False
            except Exception:
                try:
                    val1 = float(f_n.subs({n: 1000, x: pt}))
                    val2 = float(f_n.subs({n: 2000, x: pt}))
                    val3 = float(f_n.subs({n: 3000, x: pt}))
                    if abs(val1 - val2) > 1e-2 or abs(val2 - val3) > 1e-2:
                        return False
                except Exception:
                    return False
        return True
    except Exception:
        return False

def check_neg_q(witness):
    try:
        X, f_n = witness
        start = float(X.start)
        end = float(X.end)
        
        N_grid = 200
        grid = [start + i * (end - start) / N_grid for i in range(N_grid + 1)]
        
        n_values = [10, 50, 100, 500, 1000]
        max_diffs = []
        
        limit_cache = {}
        def get_limit(pt):
            pt_round = round(pt, 10)
            if pt_round in limit_cache:
                return limit_cache[pt_round]
            try:
                L_expr = sp.limit(f_n.subs(x, pt), n, sp.oo)
                if L_expr.is_finite:
                    L = float(L_expr)
                else:
                    L = float('inf')
            except Exception:
                try:
                    L = float(f_n.subs({n: 10000, x: pt}))
                except Exception:
                    L = None
            limit_cache[pt_round] = L
            return L

        for n_val in n_values:
            f_n_expr = f_n.subs(n, n_val)
            current_max_diff = 0.0
            
            pts_to_check = grid.copy()
            
            # Add boundary proximity points to catch peaks near the edges
            for power in [0.5, 1, 1.5, 2]:
                for factor in [0.1, 1.0, (end - start)]:
                    offset = factor / (n_val ** power)
                    if offset > 0:
                        pts_to_check.append(start + offset)
                        pts_to_check.append(end - offset)
                        
            # Add critical points and their proximity points
            try:
                deriv_expr = sp.diff(f_n_expr, x)
                crit_pts = sp.solve(deriv_expr, x)
                for cp in crit_pts:
                    try:
                        if not cp.free_symbols:
                            cp_val = float(cp)
                            if start <= cp_val <= end:
                                pts_to_check.append(cp_val)
                                for power in [0.5, 1, 1.5, 2]:
                                    for factor in [0.1, 1.0, (end - start)]:
                                        offset = factor / (n_val ** power)
                                        if offset > 0:
                                            pts_to_check.append(cp_val + offset)
                                            pts_to_check.append(cp_val - offset)
                    except Exception:
                        pass
            except Exception:
                pass
                
            for pt in pts_to_check:
                if pt < start or pt > end:
                    continue
                L = get_limit(pt)
                if L is None or math.isinf(L) or math.isnan(L):
                    continue
                try:
                    val = float(f_n_expr.subs(x, pt))
                    diff = abs(val - L)
                    if diff > current_max_diff:
                        current_max_diff = diff
                except Exception:
                    pass
                    
            max_diffs.append(current_max_diff)
            
        # If it does NOT converge uniformly, the max difference should remain bounded away from 0
        if len(max_diffs) >= 3:
            if max_diffs[-1] > 0.02 and max_diffs[-1] >= 0.8 * max_diffs[-3]:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    return [
        check_h1(witness),
        check_h2(witness),
        check_h3(witness),
        check_h4(witness),
        check_neg_q(witness)
    ]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: Y is a complete metric space",
    "H_3: (f_n) is a sequence of continuous functions from X to Y",
    "H_4: The sequence (f_n) converges pointwise on X",
    "¬Q: The sequence (f_n) does not converge uniformly on X"
]

N_HYP = 4
NEG_Q_INDEX = 4