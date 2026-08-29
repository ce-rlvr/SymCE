import sympy
from sympy import Symbol, Abs, limit, oo, S
from sympy.calculus.util import maximum

# Top-level setup
n = Symbol('n', integer=True, positive=True)
x = Symbol('x', real=True)

def check_uniform_convergence(f_n, f, n_var, x_var, domain):
    n_pos = Symbol('n_pos', positive=True, integer=True)
    x_real = Symbol('x_real', real=True)
    
    diff_expr = (f_n - f).subs({n_var: n_pos, x_var: x_real})
    diff_abs = Abs(diff_expr)
    
    # If the difference doesn't depend on x, it's uniform across the domain
    if not diff_abs.has(x_real):
        lim = limit(diff_abs, n_pos, oo)
        if not isinstance(lim, sympy.Limit) and lim is not sympy.nan:
            return lim == 0
        
    # Try to find the maximum absolute difference on the domain
    try:
        max_diff = maximum(diff_abs, x_real, domain)
        lim = limit(max_diff, n_pos, oo)
        if not isinstance(lim, sympy.Limit) and lim is not sympy.nan:
            if lim == 0:
                return True
            elif lim != 0:
                return False
    except Exception:
        pass
        
    # Fallback: try finding maximum of positive and negative differences separately
    try:
        max_pos = maximum(diff_expr, x_real, domain)
        max_neg = maximum(-diff_expr, x_real, domain)
        
        lim_pos = limit(max_pos, n_pos, oo)
        lim_neg = limit(max_neg, n_pos, oo)
        
        if not isinstance(lim_pos, sympy.Limit) and lim_pos is not sympy.nan and \
           not isinstance(lim_neg, sympy.Limit) and lim_neg is not sympy.nan:
            if lim_pos == 0 and lim_neg == 0:
                return True
            elif lim_pos != 0 or lim_neg != 0:
                return False
    except Exception:
        pass
        
    # Fallback: check if the difference is unbounded for a fixed n (e.g., n=1)
    try:
        max_diff_1 = maximum(diff_abs.subs(n_pos, 1), x_real, domain)
        if max_diff_1 == oo:
            return False
    except Exception:
        pass
        
    return None

def conditions(witness):
    """
    witness is expected to be a dictionary with:
      'f_n': sympy expression for the sequence of functions
      'f': sympy expression for the limit function
      'g': sympy expression for the multiplier function
      'domain': sympy Set representing the domain S
      'n': sympy Symbol for the sequence index
      'x': sympy Symbol for the spatial variable
    """
    try:
        f_n = witness['f_n']
        f = witness['f']
        g = witness['g']
        domain = witness['domain']
        n_var = witness['n']
        x_var = witness['x']
    except Exception:
        return [False, False]
        
    # H_1: (f_n) converges uniformly to f on S
    try:
        res1 = check_uniform_convergence(f_n, f, n_var, x_var, domain)
        h1_ok = (res1 is True)
    except Exception:
        h1_ok = False
        
    # neg_Q: (f_n g) does NOT converge uniformly to f g on S
    try:
        res2 = check_uniform_convergence(f_n * g, f * g, n_var, x_var, domain)
        neg_q_ok = (res2 is False)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (f_n) converges uniformly to f on S",
    "¬Q: (f_n g) does not converge uniformly to f g on S"
]

N_HYP = 1
NEG_Q_INDEX = 1