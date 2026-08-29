import sympy as sp
import math
from sympy.abc import x

def conditions(witness):
    """
    Checks if the given witness function is NOT uniformly continuous on (0, \infty).
    Returns [neg_Q_ok].
    """
    # Handle both callable functions and sympy expressions
    if callable(witness) and not isinstance(witness, sp.Expr):
        try:
            witness_expr = witness(x)
        except Exception:
            return [False]
    else:
        witness_expr = witness

    # Extract the free variable
    try:
        free_vars = witness_expr.free_symbols
        if len(free_vars) != 1:
            if len(free_vars) == 0:
                # Constant functions are uniformly continuous
                return [False]
            var = list(free_vars)[0]
        else:
            var = list(free_vars)[0]
    except Exception:
        return [False]

    def analytical_check(f_expr, v):
        """
        Returns True if definitely NOT uniformly continuous.
        Returns False if definitely IS uniformly continuous.
        Returns None if unsure.
        """
        is_continuous = False
        try:
            domain = sp.calculus.util.continuous_domain(f_expr, v, sp.Interval(0, sp.oo, True, True))
            if domain != sp.Interval(0, sp.oo, True, True):
                return True
            is_continuous = True
        except Exception:
            pass

        try:
            L0 = sp.limit(f_expr, v, 0, dir='+')
            if L0.is_infinite or L0 == sp.nan or isinstance(L0, sp.AccumBounds):
                return True
        except Exception:
            pass

        try:
            Linf = sp.limit(f_expr, v, sp.oo)
            if not (Linf.is_infinite or Linf == sp.nan or isinstance(Linf, sp.AccumBounds)):
                if is_continuous:
                    return False
        except Exception:
            pass

        try:
            df = sp.diff(f_expr, v)
            Linf_df = sp.limit(df, v, sp.oo)
            if Linf_df.is_infinite or Linf_df == sp.nan:
                return True
            if isinstance(Linf_df, sp.AccumBounds):
                if Linf_df.min == -sp.oo or Linf_df.max == sp.oo:
                    return True
                else:
                    if is_continuous:
                        return False
            else:
                if is_continuous:
                    return False
        except Exception:
            pass

        return None

    def numerical_check(f_expr, v):
        """
        Heuristic numerical check for non-uniform continuity.
        """
        try:
            f_callable = sp.lambdify(v, f_expr, modules=['math'])
        except Exception:
            return False

        deltas = [10**(-i) for i in range(2, 8)]
        epsilon = 0.05
        
        base_candidates = [10**i for i in range(-5, 5)]
        base_candidates += [i * 0.01 for i in range(1, 10000)]
        
        for delta in deltas:
            found_x = False
            candidates = base_candidates + [
                delta, delta**2, math.sqrt(delta),
                math.sqrt(delta) * 1.1, math.sqrt(delta) * 0.9,
                1.0 / math.sqrt(delta), 1.0 / delta,
                1.0 / delta + 0.5, 1.0 / delta + 1.0,
                1.0 / (delta**2) if delta >= 1e-4 else 1.0
            ]
            
            for val in candidates:
                if val <= 0: continue
                try:
                    v1 = float(f_callable(val))
                    v2 = float(f_callable(val + delta))
                    if math.isnan(v1) or math.isnan(v2) or math.isinf(v1) or math.isinf(v2):
                        continue
                    if abs(v1 - v2) > epsilon:
                        found_x = True
                        break
                except Exception:
                    pass
            
            if not found_x:
                return False
                
        return True

    try:
        ans = analytical_check(witness_expr, var)
        if ans is True:
            is_not_uc = True
        elif ans is False:
            is_not_uc = False
        else:
            is_not_uc = numerical_check(witness_expr, var)
    except Exception:
        is_not_uc = False

    return [bool(is_not_uc)]

CONDITION_LABELS = [
    r"¬Q: f is not uniformly continuous on (0, \infty)"
]

N_HYP = 0
NEG_Q_INDEX = 0