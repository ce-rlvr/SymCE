import sympy
from sympy import Symbol, Interval, S, limit, oo, Piecewise, Eq

# Top-level setup for potential witness expressions
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample to the false conjecture:
    "If F is a family of functions pointwise bounded on a topological space X, 
    then the supremum g(x) = sup_{f \in F} f(x) is continuous on X."
    
    Expected witness dictionary:
    {
      'F': sympy expression for f_n(x) (the family of functions),
      'g': sympy expression for g(x) (the supremum),
      'x': sympy Symbol for the spatial variable,
      'n': sympy Symbol for the family index,
      'domain': sympy Set representing the topological space X,
      'x0': point in domain where g is discontinuous
    }
    """
    try:
        F = witness['F']
        g = witness['g']
        x_var = witness['x']
        n_var = witness['n']
        domain = witness['domain']
        x0 = witness['x0']
    except Exception:
        return [False, False, False, False]

    # H_1: X is a topological space (we check if it's a valid subset of Reals)
    try:
        h1 = (domain.is_subset(S.Reals) == True)
    except Exception:
        h1 = False

    # H_2 & H_3: g is finite (bounded above) and is the supremum of F
    try:
        test_points = set()
        if domain.contains(x0) == True:
            test_points.add(x0)
        
        for delta in [0.1, -0.1, 0.5, -0.5, 0.01, -0.01]:
            if domain.contains(x0 + delta) == True:
                test_points.add(x0 + delta)
                
        try:
            if domain.inf.is_real and domain.contains(domain.inf) == True:
                test_points.add(domain.inf)
            if domain.sup.is_real and domain.contains(domain.sup) == True:
                test_points.add(domain.sup)
        except Exception:
            pass
            
        if not test_points:
            test_points = {0, 1, -1}

        h2 = True
        h3 = True
        for pt in test_points:
            try:
                g_val_expr = g.subs(x_var, pt).evalf()
                if not g_val_expr.is_real:
                    h2 = False
                    break
                g_val = float(g_val_expr)
            except Exception:
                h2 = False
                break
                
            is_sup = False
            for n_val in [1, 2, 3, 10, 50, 100, 1000]:
                try:
                    f_val = float(F.subs({x_var: pt, n_var: n_val}).evalf())
                    if f_val > g_val + 1e-5:
                        h2 = False
                        break
                    if abs(f_val - g_val) < 1e-5:
                        is_sup = True
                except Exception:
                    pass
            
            if not h2:
                break
                
            if not is_sup:
                try:
                    lim_expr = limit(F.subs(x_var, pt), n_var, oo).evalf()
                    if lim_expr.is_real:
                        lim = float(lim_expr)
                        if abs(lim - g_val) <= 1e-5:
                            is_sup = True
                except Exception:
                    pass

            if not is_sup:
                try:
                    from sympy.calculus.util import maximum
                    max_val = maximum(F.subs(x_var, pt), n_var, S.Naturals)
                    if max_val.is_real:
                        if abs(float(max_val.evalf()) - g_val) <= 1e-5:
                            is_sup = True
                except Exception:
                    pass

            if not is_sup:
                try:
                    f_val_large = float(F.subs({x_var: pt, n_var: 10000}).evalf())
                    if abs(f_val_large - g_val) <= 1e-4:
                        is_sup = True
                except Exception:
                    pass

            if not is_sup:
                h3 = False
                break
    except Exception:
        h2 = False
        h3 = False

    # ¬Q: g is not continuous on X (specifically at x0)
    try:
        g_x0 = float(g.subs(x_var, x0).evalf())
        is_continuous = True
        
        check_left = False
        try:
            if domain.contains(x0 - 1e-5) == True:
                check_left = True
        except Exception:
            check_left = True

        if check_left:
            lim_success = False
            try:
                lim_left = limit(g, x_var, x0, dir='-').evalf()
                if not lim_left.is_real or abs(float(lim_left) - g_x0) > 1e-5:
                    is_continuous = False
                lim_success = True
            except Exception:
                pass
            
            if not lim_success:
                try:
                    val_left = float(g.subs(x_var, x0 - 1e-7).evalf())
                    if abs(val_left - g_x0) > 1e-3:
                        is_continuous = False
                except Exception:
                    pass

        check_right = False
        try:
            if domain.contains(x0 + 1e-5) == True:
                check_right = True
        except Exception:
            check_right = True

        if check_right:
            lim_success = False
            try:
                lim_right = limit(g, x_var, x0, dir='+').evalf()
                if not lim_right.is_real or abs(float(lim_right) - g_x0) > 1e-5:
                    is_continuous = False
                lim_success = True
            except Exception:
                pass
            
            if not lim_success:
                try:
                    val_right = float(g.subs(x_var, x0 + 1e-7).evalf())
                    if abs(val_right - g_x0) > 1e-3:
                        is_continuous = False
                except Exception:
                    pass

        neg_q = not is_continuous
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: For each x in X, F is bounded above",
    "H_3: g is the supremum of F",
    "¬Q: g is not continuous on X"
]
N_HYP = 3
NEG_Q_INDEX = 3