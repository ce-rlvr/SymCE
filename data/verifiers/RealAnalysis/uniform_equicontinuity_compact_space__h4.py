import sympy as sp
from sympy import Symbol, Interval, Set, Expr, Tuple
from sympy.abc import x, y, z, t, n, k, m
import math

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: Y is a metric space",
    "H_3: F is a family of functions from X to Y",
    "¬Q: F is not uniformly equicontinuous on X"
]
N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Default values
    X_set = None
    F = None
    
    try:
        if isinstance(witness, (tuple, Tuple, list)) and len(witness) == 2:
            X_set, F = witness
        else:
            X_set = Interval(0, 1)
            F = witness
    except Exception:
        pass

    # H_1: X is a compact metric space
    try:
        h1 = False
        if isinstance(X_set, Interval):
            if not X_set.inf.is_infinite and not X_set.sup.is_infinite:
                if X_set.left_open is False and X_set.right_open is False:
                    h1 = True
    except Exception:
        h1 = False

    # H_2: Y is a metric space
    # We assume Y is R, which is a metric space.
    h2 = True

    # H_3: F is a family of functions from X to Y
    try:
        h3 = False
        def is_well_defined(expr, var, val):
            try:
                res = expr.subs(var, val)
                if res.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                    return False
                if res.is_real is False:
                    return False
                return True
            except Exception:
                return False

        if isinstance(F, Expr):
            spatial_vars = [sym for sym in F.free_symbols if sym.name not in ['n', 'k', 'm', 'i', 'j']]
            if len(spatial_vars) <= 1:
                spatial_var = spatial_vars[0] if spatial_vars else x
                if X_set is not None and hasattr(X_set, 'inf') and hasattr(X_set, 'sup'):
                    if is_well_defined(F, spatial_var, X_set.inf) and is_well_defined(F, spatial_var, X_set.sup):
                        h3 = True
        elif isinstance(F, (list, tuple, Tuple)):
            h3 = True
            for f in F:
                if not isinstance(f, Expr):
                    h3 = False
                    break
                spatial_vars = [sym for sym in f.free_symbols if sym.name not in ['n', 'k', 'm', 'i', 'j']]
                spatial_var = spatial_vars[0] if spatial_vars else x
                if X_set is not None and hasattr(X_set, 'inf') and hasattr(X_set, 'sup'):
                    if not (is_well_defined(f, spatial_var, X_set.inf) and is_well_defined(f, spatial_var, X_set.sup)):
                        h3 = False
                        break
    except Exception:
        h3 = False

    # neg_Q: F is not uniformly equicontinuous on X
    try:
        neg_q = False
        inf_val = X_set.inf if X_set is not None and hasattr(X_set, 'inf') else 0.0
        sup_val = X_set.sup if X_set is not None and hasattr(X_set, 'sup') else 1.0
        
        if inf_val.has(sp.oo, -sp.oo) or sup_val.has(sp.oo, -sp.oo):
            inf = -10.0
            sup = 10.0
        else:
            inf = float(inf_val)
            sup = float(sup_val)
            
        eps = 0.1
        deltas = [0.1, 0.01, 0.001, 0.0001, 1e-5, 1e-6]
        
        f_lambdas = []
        
        if isinstance(F, Expr):
            index_vars = [sym for sym in F.free_symbols if sym.name in ['n', 'k', 'm', 'i', 'j']]
            spatial_vars = [sym for sym in F.free_symbols if sym.name not in ['n', 'k', 'm', 'i', 'j']]
            spatial_var = spatial_vars[0] if spatial_vars else x
            index_var = index_vars[0] if index_vars else None
            
            if index_var:
                for n_val in [1, 2, 5, 10, 50, 100, 1000, 10000, 100000, 10**6, 10**7]:
                    f_sub = F.subs(index_var, n_val)
                    f_lambdas.append(sp.lambdify(spatial_var, f_sub, modules=['math']))
            else:
                f_lambdas.append(sp.lambdify(spatial_var, F, modules=['math']))
        elif isinstance(F, (list, tuple, Tuple)):
            spatial_vars = set()
            for f in F:
                if isinstance(f, Expr):
                    spatial_vars.update([sym for sym in f.free_symbols])
            spatial_var = list(spatial_vars)[0] if spatial_vars else x
            f_lambdas = [sp.lambdify(spatial_var, f, modules=['math']) for f in F if isinstance(f, Expr)]
        
        if f_lambdas:
            all_deltas_fail = True
            for delta in deltas:
                found_violation = False
                points = [inf, sup]
                for i in range(1, 100):
                    points.append(inf + i * (sup - inf) / 100)
                    points.append(sup - i * (sup - inf) / 100)
                for k_pow in range(1, 7):
                    offset = (sup - inf) * (10.0**-k_pow)
                    points.append(inf + offset)
                    points.append(sup - offset)
                    
                points = sorted(list(set(points)))
                points = [p for p in points if inf <= p <= sup]
                
                for f_lam in f_lambdas:
                    if found_violation:
                        break
                    for pt in points:
                        pt_test = pt
                        pt2 = pt_test + delta * 0.9
                        if pt2 > sup:
                            pt2 = pt_test - delta * 0.9
                        if pt2 < inf:
                            pt2 = sup
                            pt_test = inf
                        try:
                            val1 = f_lam(pt_test)
                            val2 = f_lam(pt2)
                            if abs(val1 - val2) >= eps:
                                found_violation = True
                                break
                        except Exception:
                            pass
                if not found_violation:
                    all_deltas_fail = False
                    break
            neg_q = all_deltas_fail
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]