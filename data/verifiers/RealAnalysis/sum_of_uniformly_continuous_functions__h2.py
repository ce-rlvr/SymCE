import sympy
from sympy import Symbol, S, Interval, oo, limit, diff, Poly, Expr, Set

try:
    from sympy import continuous_domain, maximum
except ImportError:
    from sympy.calculus.util import continuous_domain, maximum

# Top-level setup
x = Symbol('x', real=True)

def is_uniformly_continuous(expr, domain, x):
    expr = sympy.sympify(expr)
    if not isinstance(expr, Expr):
        raise ValueError("Not an expression")
        
    # 1. Check continuity
    try:
        cd = continuous_domain(expr, x, domain)
        subset_check = domain.is_subset(cd)
        if subset_check is False:
            return False
        elif subset_check is None:
            raise ValueError("Cannot determine continuous domain")
    except Exception:
        raise ValueError("Error in continuous_domain")
        
    # 2. Finite closed interval -> uniformly continuous
    if getattr(domain, 'is_Interval', False) and not domain.left_open and not domain.right_open:
        if (domain.measure < oo) == True:
            return True
            
    # 2.5 Check limits at open endpoints for unbounded behavior
    try:
        if getattr(domain, 'left_open', False) and domain.inf != -oo:
            L = limit(expr, x, domain.inf, dir='+')
            if L == oo or L == -oo or L == sympy.zoo:
                return False
        if getattr(domain, 'right_open', False) and domain.sup != oo:
            L = limit(expr, x, domain.sup, dir='-')
            if L == oo or L == -oo or L == sympy.zoo:
                return False
    except Exception:
        pass

    # 3. Check if it's a polynomial
    try:
        p = Poly(expr, x)
        if p.degree() <= 1:
            return True
        if p.degree() > 1 and (getattr(domain, 'measure', None) == oo) == True:
            return False
    except Exception:
        pass
        
    # 4. Check derivative boundedness
    try:
        dexpr = diff(expr, x)
        if dexpr.is_constant():
            return True
            
        # 5. Limit of derivative at infinity for unbounded domains
        if (getattr(domain, 'measure', None) == oo) == True:
            if domain.sup == oo:
                L = limit(dexpr, x, oo)
                if L == oo or L == -oo or L == sympy.zoo:
                    return False
            if domain.inf == -oo:
                L = limit(dexpr, x, -oo)
                if L == oo or L == -oo or L == sympy.zoo:
                    return False

        # 6. Try maximum of derivative
        max_val = maximum(abs(dexpr), x, domain)
        if (max_val < oo) == True:
            return True
    except Exception:
        pass

    # If we can't determine, raise an exception to fail safely
    raise ValueError("Cannot determine uniform continuity")

def conditions(witness):
    """
    witness is expected to be a tuple: (X, f, g)
    where X is a sympy Set (the metric space domain),
    and f, g are sympy expressions in terms of x.
    """
    try:
        X, f, g = witness
        f = sympy.sympify(f)
        g = sympy.sympify(g)
    except Exception:
        return [False, False, False]
        
    # H_1: X is a metric space
    try:
        h1_ok = isinstance(X, Set)
    except Exception:
        h1_ok = False
        
    # H_2: g is uniformly continuous on X
    try:
        h2_ok = is_uniformly_continuous(g, X, x)
    except Exception:
        h2_ok = False
        
    # neg_Q: f + g is NOT uniformly continuous on X
    try:
        neg_q_ok = not is_uniformly_continuous(f + g, X, x)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: g is uniformly continuous on X",
    "¬Q: f + g is not uniformly continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2