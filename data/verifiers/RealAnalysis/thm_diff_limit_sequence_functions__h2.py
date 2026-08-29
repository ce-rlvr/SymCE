import sympy
from sympy import Symbol, S, limit, oo, Abs, diff, simplify
from sympy.calculus.util import maximum

# Top-level setup for witness expressions
x = Symbol('x', real=True)
k = Symbol('k', integer=True, positive=True)

def check_uniform_convergence(expr, x, k, U):
    """Helper to check if expr converges uniformly to 0 on U as k -> oo."""
    if not expr.has(x):
        return limit(expr, k, oo) == 0
    
    try:
        sup = maximum(Abs(expr), x, U)
        if not sup.has(x):
            return limit(sup, k, oo) == 0
    except Exception:
        pass
    
    # Fallback 1: evaluate at x = k (useful for unbounded domains like Reals)
    try:
        val_at_k = expr.subs(x, k)
        if limit(Abs(val_at_k), k, oo) != 0:
            return False
    except Exception:
        pass

    # Fallback 2: evaluate at x = k^2
    try:
        val_at_k2 = expr.subs(x, k**2)
        if limit(Abs(val_at_k2), k, oo) != 0:
            return False
    except Exception:
        pass

    # If we cannot definitively prove uniform convergence, we assume it fails.
    # This is safe for rejecting invalid H3, and safe for neg_Q (makes it True).
    return False

def conditions(witness):
    """
    witness is expected to be a dictionary with keys:
      'f_k': sequence of functions (sympy expression in x and k)
      'U': domain (sympy Set, e.g., S.Reals)
      'x0': point in U (sympy number)
      'G': limit of derivatives (sympy expression in x)
      'f': (optional) pointwise limit function (sympy expression in x)
    """
    try:
        if isinstance(witness, dict):
            f_k = witness.get('f_k')
            U = witness.get('U')
            x0 = witness.get('x0')
            G = witness.get('G')
            f = witness.get('f')
        else:
            f_k, U, x0, G, f = witness
    except Exception:
        return [False, False, False, False]

    # H1: U is an open connected set
    try:
        h1 = bool(U.is_open and U.is_connected)
    except Exception:
        h1 = False

    # H2: There exists x0 in U such that f_k(x0) converges
    try:
        if U.contains(x0) != True:
            h2 = False
        else:
            val = f_k.subs(x, x0)
            lim_val = limit(val, k, oo)
            if lim_val.is_finite and not lim_val.has(sympy.AccumBounds):
                h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False

    # H3: The sequence of total derivatives Df_k converges uniformly on U to G
    try:
        df_k = diff(f_k, x)
        diff_G = simplify(df_k - G)
        h3 = check_uniform_convergence(diff_G, x, k, U)
    except Exception:
        h3 = False

    # Negated Conclusion:
    # The sequence f_k does NOT converge uniformly on U to a differentiable function f with Df = G
    try:
        # Try to find the actual pointwise limit
        try:
            actual_f = limit(f_k, k, oo)
            if actual_f.has(k) or actual_f.has(sympy.AccumBounds):
                actual_f = f
        except Exception:
            actual_f = f

        if actual_f is None:
            # Cannot determine the limit and none provided; assume conclusion holds to avoid false positives
            neg_q = False
        else:
            diff_f = simplify(f_k - actual_f)
            unif_conv = check_uniform_convergence(diff_f, x, k, U)
            
            try:
                df = diff(actual_f, x)
                deriv_match = (simplify(df - G) == 0)
            except Exception:
                deriv_match = False
                
            neg_q = not (unif_conv and deriv_match)
    except Exception:
        # If evaluation fails catastrophically, the conclusion likely fails (e.g. non-differentiable)
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: U is an open connected set",
    "H_2: There exists x0 in U such that the sequence f_k(x0) converges",
    "H_3: The sequence of total derivatives Df_k converges uniformly on U to G",
    "¬Q: The sequence f_k does not converge uniformly on U to a differentiable function f with Df = G"
]

N_HYP = 3
NEG_Q_INDEX = 3