import sympy as sp

# Top-level setup for Real Analysis
x, y, z, t = sp.symbols('x y z t', real=True)
n, m, k, N = sp.symbols('n m k N', integer=True, positive=True)

def check_limit_zero(val, n_var):
    try:
        lim = sp.limit(val, n_var, sp.oo)
        if lim == 0:
            return True
        if lim.is_number and lim > 0:
            return False
        if lim == sp.oo or lim == -sp.oo:
            return False
    except Exception:
        pass
    return None

def check_uniform_convergence(expr, limit_expr, n_var, x_var, domain):
    inner_expr = expr - limit_expr
    
    # 1. Check if domain is a FiniteSet
    if isinstance(domain, sp.FiniteSet):
        try:
            all_zero = True
            for pt in domain:
                val = sp.Abs(inner_expr.subs(x_var, pt))
                res = check_limit_zero(val, n_var)
                if res is False:
                    return False
                if res is None:
                    all_zero = False
            if all_zero:
                return True
        except Exception:
            pass

    diff_expr = sp.Abs(inner_expr)

    # 2. Try exact maximum over the domain
    try:
        max_val = sp.calculus.util.maximum(diff_expr, x_var, domain)
        lim_check = check_limit_zero(max_val, n_var)
        if lim_check is not None:
            return lim_check
    except Exception:
        pass
        
    # 3. Try evaluating at critical points and endpoints
    try:
        deriv = sp.diff(inner_expr, x_var)
        crit_points = sp.solve(deriv, x_var)
        
        points_to_check = list(crit_points)
        if isinstance(domain, sp.Interval):
            points_to_check.extend([domain.start, domain.end])
            
        all_zero = True
        for pt in points_to_check:
            val = sp.Abs(inner_expr.subs(x_var, pt))
            res = check_limit_zero(val, n_var)
            if res is False:
                return False
            if res is None:
                all_zero = False
        if all_zero:
            return True
    except Exception:
        pass
        
    return None

def conditions(witness):
    """
    witness can be a dict or a tuple.
    Expected dict keys: 'f_expr', 'S_expr', 'domain', 'x_var', 'n_var'
    Optional dict keys: 'partial_sum', 'N_var'
    Expected tuple: (f_expr, S_expr, domain, x_var, n_var)
    Optional tuple: (f_expr, S_expr, domain, x_var, n_var, partial_sum, N_var)
    """
    try:
        if isinstance(witness, dict):
            f_expr = witness['f_expr']
            S_expr = witness['S_expr']
            domain = witness['domain']
            x_var = witness['x_var']
            n_var = witness['n_var']
            if 'partial_sum' in witness and 'N_var' in witness:
                partial_sum = witness['partial_sum']
                N_var = witness['N_var']
            else:
                N_var = sp.Symbol('N', integer=True, positive=True)
                partial_sum = sp.Sum(f_expr, (n_var, 1, N_var)).doit()
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                f_expr, S_expr, domain, x_var, n_var = witness
                N_var = sp.Symbol('N', integer=True, positive=True)
                partial_sum = sp.Sum(f_expr, (n_var, 1, N_var)).doit()
            elif len(witness) == 7:
                f_expr, S_expr, domain, x_var, n_var, partial_sum, N_var = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: f_n(x) is a series of real-valued functions defined on X
    try:
        h1 = isinstance(f_expr, sp.Expr) and isinstance(S_expr, sp.Expr) and isinstance(domain, sp.Set)
    except Exception:
        h1 = False
        
    # H2: The series converges uniformly to S(x) on X
    try:
        h2_val = check_uniform_convergence(partial_sum, S_expr, N_var, x_var, domain)
        h2 = (h2_val is True)
    except Exception:
        h2 = False
        
    # neg_Q: The sequence of remainder functions R_N does not converge uniformly to 0 on X
    try:
        R_N = S_expr - partial_sum
        q_val = check_uniform_convergence(R_N, sp.S(0), N_var, x_var, domain)
        if q_val is None:
            neg_q = False
        else:
            neg_q = not q_val
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f_n(x) is a series of real-valued functions defined on X",
    "H_2: The series converges uniformly to S(x) on X",
    "¬Q: The sequence of remainder functions R_N does not converge uniformly to 0 on X"
]

N_HYP = 2
NEG_Q_INDEX = 2