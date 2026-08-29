import sympy
from sympy import Symbol, Interval, oo, S, diff, limit, Poly
from sympy.calculus.util import continuous_domain
from sympy import AccumBounds

x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    Witness is expected to be a tuple (f, g, a) or a dict with keys 'f', 'g', 'a'.
    f and g are sympy expressions in terms of x, and a is a real number.
    """
    if isinstance(witness, dict):
        f = witness.get('f', x**2)
        g = witness.get('g', S.Zero)
        a = witness.get('a', S.Zero)
    else:
        f, g, a = witness

    # H1: f and g are continuous on [a, oo)
    def is_continuous(expr):
        try:
            domain = continuous_domain(expr, x, S.Reals)
            return bool(Interval(a, oo).is_subset(domain))
        except Exception:
            return False

    try:
        h1_ok = is_continuous(f) and is_continuous(g)
    except Exception:
        h1_ok = False

    # H2: g is uniformly continuous on [a, oo)
    def is_uniformly_continuous(expr):
        try:
            dg = diff(expr, x)
            if dg.is_constant():
                return True
            
            # Heuristic 1: Check limit of f(x + 1/x) - f(x) as x -> oo
            # If f is uniformly continuous, this limit must be 0.
            diff_expr = expr.subs(x, x + 1/x) - expr
            L = limit(diff_expr, x, oo)
            if not (L == 0):
                return False
                
            # Heuristic 2: Check limit of derivative as x -> oo
            # If the derivative goes to infinity, it's not uniformly continuous.
            L_dg = limit(dg, x, oo)
            if L_dg == oo or L_dg == -oo:
                return False
            
            if isinstance(L_dg, AccumBounds):
                if L_dg.min == -oo or L_dg.max == oo:
                    return False
                
            # Heuristic 3: If it's a polynomial, degree must be <= 1
            try:
                p = Poly(expr, x)
                if p.degree() <= 1:
                    return True
                else:
                    return False
            except Exception:
                pass
                
            # If it passes the necessary conditions and isn't a high-degree polynomial,
            # we assume it is uniformly continuous (sufficient for standard counterexamples).
            return True
        except Exception:
            return False

    try:
        h2_ok = bool(is_uniformly_continuous(g))
    except Exception:
        h2_ok = False

    # neg_Q: f is NOT uniformly continuous on [a, oo)
    try:
        neg_q_ok = not bool(is_uniformly_continuous(f))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f and g are continuous functions from [a, oo) to R",
    "H_2: g is uniformly continuous on [a, oo)",
    "¬Q: f is not uniformly continuous on [a, oo)"
]

N_HYP = 2
NEG_Q_INDEX = 2