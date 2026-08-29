import sympy
from sympy import Symbol, S, sin, cos, tan, exp, log, pi, Interval, oo, diff, maximum, minimum, limit
from sympy.calculus.util import function_range, continuous_domain

# Top-level setup
x = Symbol('x', real=True)

def is_bounded(expr, D, sym):
    try:
        if expr.is_constant():
            return True
    except Exception:
        pass

    # Heuristic for unboundedness to prevent hanging on complex expressions
    points = [0, 1, -1, 2, -2, 3, -3, 5, -5, 10, -10, 50, -50, 100, -100, 500, -500, 1000, -1000, 10000, -10000]
    points += [k * pi for k in [1, 2, 3, 4, 5, 10, 100, 1000, 10000, -10, -100, -1000, -10000]]
    points += [k * pi / 2 for k in [1, 3, 5, 7, 11, 101, 1001, 10001, -11, -101, -1001, -10001]]
    
    max_val = 0
    for p in points:
        try:
            if D.contains(p) == True:
                val = abs(float(expr.subs(sym, p).evalf()))
                if val > 1000:
                    return False
                if val > max_val:
                    max_val = val
        except Exception:
            pass

    # Try formal methods
    try:
        fr = function_range(expr, sym, D)
        if fr.is_subset(S.Reals):
            return fr.is_bounded
    except Exception:
        pass

    try:
        M = maximum(expr, sym, D)
        m = minimum(expr, sym, D)
        if M == oo or m == -oo:
            return False
        if M.is_finite and m.is_finite:
            return True
    except Exception:
        pass

    # If formal methods fail, check limits at infinity
    try:
        if D.sup == oo:
            L = limit(expr, sym, oo)
            if L == oo or L == -oo:
                return False
    except Exception:
        pass

    try:
        if D.inf == -oo:
            L = limit(expr, sym, -oo)
            if L == oo or L == -oo:
                return False
    except Exception:
        pass

    # Fallback to True to avoid rejecting valid hypotheses
    return True

def is_uniformly_continuous(expr, D, sym):
    # Must be continuous on D
    try:
        cd = continuous_domain(expr, sym, S.Reals)
        if not D.is_subset(cd):
            return False
    except Exception:
        pass

    try:
        dexpr = diff(expr, sym)
    except Exception:
        return False
        
    # If derivative is bounded on D, it is uniformly continuous
    if is_bounded(dexpr, D, sym):
        return True
        
    # If D is a bounded closed interval and expr is continuous, it is uniformly continuous
    try:
        if D.is_Interval and D.left_open == False and D.right_open == False and D.measure < oo:
            return True
    except Exception:
        pass

    # Check if limit of derivative at infinity is 0 (e.g., for sqrt(x))
    try:
        if D.sup == oo:
            lim_inf = limit(dexpr, sym, oo)
            if lim_inf == 0:
                return True
    except Exception:
        pass

    try:
        if D.inf == -oo:
            lim_ninf = limit(dexpr, sym, -oo)
            if lim_ninf == 0:
                return True
    except Exception:
        pass

    return False

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    Witness is expected to be a tuple: (f, g, D)
    where f and g are sympy expressions and D is a sympy Set.
    """
    try:
        f, g, D = witness
    except Exception:
        return [False, False, False, False]

    try:
        syms = set()
        if hasattr(f, 'free_symbols'):
            syms.update(f.free_symbols)
        if hasattr(g, 'free_symbols'):
            syms.update(g.free_symbols)
        syms = {s for s in syms if s.is_Symbol}
        sym = list(syms)[0] if syms else x
    except Exception:
        sym = x

    try:
        h1 = bool(is_uniformly_continuous(f, D, sym))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_uniformly_continuous(g, D, sym))
    except Exception:
        h2 = False

    try:
        h3 = bool(is_bounded(f, D, sym))
    except Exception:
        h3 = False

    try:
        fg = f * g
        q = is_uniformly_continuous(fg, D, sym)
        neg_q = not bool(q)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is uniformly continuous on D",
    "H_2: g is uniformly continuous on D",
    "H_3: f is bounded on D",
    "¬Q: fg is not uniformly continuous on D"
]

N_HYP = 3
NEG_Q_INDEX = 3