import sympy
from sympy import Symbol, Interval, Union, S, oo, limit, Abs, diff, solve, sympify
from sympy.calculus.util import maximum, continuous_domain

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def check_uniform_convergence(f_n, f, x_sym, n_sym, domain):
    expr = Abs(f_n - f)
    
    # 1. Try symbolic maximum
    try:
        M = maximum(expr, x_sym, domain)
        lim = limit(M, n_sym, oo)
        if lim == 0:
            return True
        elif lim > 0 or lim == oo:
            return False
    except Exception:
        pass
        
    # 2. Fallback: evaluate at critical points and boundaries
    points = []
    try:
        deriv = diff(expr, x_sym)
        crit = solve(deriv, x_sym)
        points.extend(crit)
    except Exception:
        pass
        
    def get_boundaries(dom):
        bnd = []
        if hasattr(dom, 'is_Interval') and dom.is_Interval:
            bnd.extend([dom.start, dom.end])
        elif dom == S.Reals:
            bnd.extend([-oo, oo])
        elif hasattr(dom, 'is_Union') and dom.is_Union:
            for arg in dom.args:
                bnd.extend(get_boundaries(arg))
        elif hasattr(dom, 'is_FiniteSet') and dom.is_FiniteSet:
            bnd.extend(list(dom))
        return bnd
        
    points.extend(get_boundaries(domain))
    
    max_lim = S.NegativeInfinity
    for p in points:
        try:
            # Check if p is in domain for large n
            p_lim = limit(p, n_sym, oo)
            if p_lim.is_comparable or p_lim in [oo, -oo]:
                in_domain = False
                try:
                    if domain.contains(p_lim) == True:
                        in_domain = True
                    elif hasattr(domain, 'boundary') and domain.boundary.contains(p_lim) == True:
                        in_domain = True
                    elif p_lim == oo and getattr(domain, 'sup', None) == oo:
                        in_domain = True
                    elif p_lim == -oo and getattr(domain, 'inf', None) == -oo:
                        in_domain = True
                except Exception:
                    in_domain = True
                    
                if not in_domain:
                    continue
                    
            val = limit(expr, x_sym, p)
            lim_n = limit(val, n_sym, oo)
            if lim_n.is_comparable and lim_n > max_lim:
                max_lim = lim_n
        except Exception:
            pass
            
    if max_lim == 0:
        return True
    elif max_lim > 0 or max_lim == oo:
        return False
        
    # 3. Numerical fallback for bounded intervals
    try:
        if hasattr(domain, 'is_Interval') and domain.is_Interval and domain.start.is_finite and domain.end.is_finite:
            start = float(domain.start)
            end = float(domain.end)
            grid = [start + i*(end-start)/100 for i in range(101)]
            
            max_vals = []
            for n_val in [100, 1000]:
                expr_n = expr.subs(n_sym, n_val)
                m = max(float(expr_n.subs(x_sym, p)) for p in grid)
                max_vals.append(m)
                
            if max_vals[-1] < 1e-3 and max_vals[-1] < max_vals[0]:
                return True
            elif max_vals[-1] > 0.1:
                return False
    except Exception:
        pass
        
    return None

def conditions(witness):
    A = witness.get("A")
    B = witness.get("B")
    f_n_raw = witness.get("f_n")
    f_raw = witness.get("f")
    
    # H1: A and B are subsets of R
    h1_ok = False
    try:
        if hasattr(A, 'is_subset') and hasattr(B, 'is_subset'):
            if A.is_subset(S.Reals) and B.is_subset(S.Reals):
                h1_ok = True
    except Exception:
        pass
        
    # H2: f_n is defined on A U B
    h2_ok = False
    try:
        f_n = sympify(f_n_raw)
        f = sympify(f_raw)
        if hasattr(f_n, 'subs') and hasattr(f, 'subs'):
            h2_ok = True
            A_U_B = Union(A, B)
            f_1 = f_n.subs(n, 1)
            dom = continuous_domain(f_1, x, S.Reals)
            if not A_U_B.is_subset(dom):
                h2_ok = False
            else:
                f_limit = f.subs(n, 1) if f.has(n) else f
                dom_f = continuous_domain(f_limit, x, S.Reals)
                if not A_U_B.is_subset(dom_f):
                    h2_ok = False
    except Exception:
        pass
        
    # H3: f_n converges uniformly to f on A
    h3_ok = False
    try:
        if h1_ok and h2_ok:
            res = check_uniform_convergence(f_n, f, x, n, A)
            if res is True:
                h3_ok = True
    except Exception:
        pass
        
    # neg_Q: f_n does NOT converge uniformly to f on A U B
    neg_q_ok = False
    try:
        if h1_ok and h2_ok:
            A_U_B = Union(A, B)
            res = check_uniform_convergence(f_n, f, x, n, A_U_B)
            if res is False:
                neg_q_ok = True
    except Exception:
        pass
        
    return [bool(h1_ok), bool(h2_ok), bool(h3_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: A and B are subsets of R",
    "H_2: {f_n} is a sequence of functions defined on A U B",
    "H_3: {f_n} converges uniformly to f on A",
    "¬Q: {f_n} does not converge uniformly to f on A U B"
]

N_HYP = 3
NEG_Q_INDEX = 3