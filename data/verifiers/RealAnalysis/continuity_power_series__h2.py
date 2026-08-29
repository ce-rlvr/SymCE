import sympy as sp

n = sp.Symbol('n', integer=True, nonnegative=True)
x = sp.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: f(x) = sum a_n (x-c)^n is a power series",
    "¬Q: f(x) is not continuous on (c-R, c+R)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    witness is expected to be a tuple: (a_n, c, R)
    where:
      - a_n is a sympy expression for the n-th coefficient (in terms of n)
      - c is the center of the power series (real number)
      - R is the radius of the interval to check for continuity
    """
    try:
        a_n, c, R = witness
    except Exception:
        return [False, False]
    
    # H_1: Check if it's a valid power series definition
    try:
        a_n_expr = sp.sympify(a_n)
        # Ensure we use our specific 'n' with assumptions
        for sym in a_n_expr.free_symbols:
            if sym.name == 'n':
                a_n_expr = a_n_expr.subs(sym, n)
                
        c_val = sp.sympify(c)
        R_val = sp.sympify(R)
        
        # c and R must be real numbers (or R can be infinity)
        h1 = (c_val.is_real is not False) and (R_val.is_real is not False or R_val is sp.oo)
        
        # The coefficient sequence should only depend on n
        if not a_n_expr.free_symbols.issubset({n}):
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: f(x) is NOT continuous on (c-R, c+R)
    # This happens if the interval (c-R, c+R) is valid (R > 0) and extends beyond the radius of convergence R_c.
    try:
        if a_n_expr == 0:
            R_c = sp.oo
        else:
            # Try the root test first to find the radius of convergence
            root = sp.Abs(a_n_expr)**(1/n)
            L = sp.limit(root, n, sp.oo)
            
            if isinstance(L, sp.Limit) or L.has(sp.AccumBounds) or L is sp.nan:
                # Fallback to the ratio test if the root test limit is unevaluated or indeterminate
                ratio = sp.Abs(a_n_expr / a_n_expr.subs(n, n+1))
                R_c = sp.limit(ratio, n, sp.oo)
            else:
                if L == 0:
                    R_c = sp.oo
                elif L == sp.oo:
                    R_c = 0
                else:
                    R_c = 1 / L
                    
        # The conclusion fails if the specified R is strictly greater than the actual radius of convergence
        neg_q = bool(R_val > 0) and bool(R_val > R_c)
    except Exception:
        neg_q = False

    return [h1, neg_q]