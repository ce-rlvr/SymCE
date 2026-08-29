import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)

def is_not_uc(expr, x_sym):
    """
    Heuristically checks if a sympy expression is NOT uniformly continuous.
    Returns True if it can confidently determine it is not uniformly continuous.
    """
    try:
        # 1. Check finite differences in the positive direction
        diffs = []
        for v in [10, 100, 1000, 10000, 100000]:
            try:
                val1 = float(expr.subs(x_sym, v + 1).evalf())
                val0 = float(expr.subs(x_sym, v).evalf())
                if not math.isnan(val1) and not math.isnan(val0):
                    diffs.append(abs(val1 - val0))
            except Exception:
                pass
        if len(diffs) >= 3 and max(diffs) > 1000 and max(diffs) > 10 * min(diffs):
            return True
            
        # 2. Check finite differences in the negative direction
        diffs_neg = []
        for v in [-10, -100, -1000, -10000, -100000]:
            try:
                val1 = float(expr.subs(x_sym, v - 1).evalf())
                val0 = float(expr.subs(x_sym, v).evalf())
                if not math.isnan(val1) and not math.isnan(val0):
                    diffs_neg.append(abs(val1 - val0))
            except Exception:
                pass
        if len(diffs_neg) >= 3 and max(diffs_neg) > 1000 and max(diffs_neg) > 10 * min(diffs_neg):
            return True
            
        # 3. Check numerical derivative for unboundedness (e.g., sin(x^2))
        derivs = []
        for v in [10, 100, 1000, 10000]:
            try:
                local_derivs = []
                for offset in [0.1, 0.2, 0.3]:
                    delta = 1e-5
                    val1 = float(expr.subs(x_sym, v + offset + delta).evalf())
                    val0 = float(expr.subs(x_sym, v + offset).evalf())
                    if not math.isnan(val1) and not math.isnan(val0):
                        local_derivs.append(abs(val1 - val0) / delta)
                if local_derivs:
                    derivs.append(max(local_derivs))
            except Exception:
                pass
        if len(derivs) >= 3 and max(derivs) > 1000 and max(derivs) > 10 * min(derivs):
            return True
            
    except Exception:
        pass
    return False

def is_uc(expr, x_sym, domain=sp.S.Reals):
    """
    Heuristically checks if a sympy expression is uniformly continuous.
    """
    try:
        if expr.is_constant():
            return True
    except Exception:
        pass
        
    try:
        if expr.is_polynomial(x_sym):
            return sp.degree(expr, x_sym) <= 1
    except Exception:
        pass
        
    try:
        if sp.calculus.util.continuous_domain(expr, x_sym, domain) != domain:
            return False
    except Exception:
        pass
        
    # If it's continuous on the domain and not caught by the non-UC heuristic, assume it's UC
    return not is_not_uc(expr, x_sym)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    f_expr = None
    g_expr = None
    domain = sp.S.Reals
    
    try:
        if isinstance(witness, dict):
            f_expr = witness.get('f')
            g_expr = witness.get('g')
            if 'domain' in witness:
                domain = witness['domain']
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                domain, f_expr, g_expr = witness
            elif len(witness) == 2:
                f_expr, g_expr = witness
    except Exception:
        pass
        
    if f_expr is None or g_expr is None:
        return [False, False, False]
        
    try:
        f_expr = sp.sympify(f_expr)
        g_expr = sp.sympify(g_expr)
        symbols = f_expr.free_symbols | g_expr.free_symbols
        if len(symbols) == 1:
            x_sym = list(symbols)[0]
        elif len(symbols) == 0:
            x_sym = x
        else:
            if x in symbols:
                x_sym = x
            else:
                x_sym = list(symbols)[0]
    except Exception:
        return [False, False, False]

    # H1: X is a metric space
    h1_ok = True
    if domain != sp.S.Reals:
        try:
            if not isinstance(domain, sp.Set):
                h1_ok = False
        except Exception:
            h1_ok = False
            
    # H2: f is uniformly continuous on X
    h2_ok = False
    try:
        h2_ok = is_uc(f_expr, x_sym, domain)
    except Exception:
        pass
        
    # neg_Q: h(x) = max(f(x), g(x)) is NOT uniformly continuous on X
    neg_q_ok = False
    try:
        h_expr = sp.Max(f_expr, g_expr)
        neg_q_ok = is_not_uc(h_expr, x_sym)
    except Exception:
        pass
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: f is uniformly continuous on X",
    "¬Q: h(x) = max(f(x), g(x)) is NOT uniformly continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2