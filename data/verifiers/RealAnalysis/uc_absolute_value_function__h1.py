import sympy
from sympy import Symbol, Abs, S, diff, limit, oo, Interval, AccumBounds
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

def is_uniformly_continuous(f, X):
    """
    Heuristic check for uniform continuity of a sympy expression f on a set X.
    """
    try:
        # Must be continuous on the domain
        if continuous_domain(f, x, X) != X:
            return False
            
        # Check boundaries for intervals
        if isinstance(X, Interval):
            if X.start.is_finite and X.left_open:
                L = limit(f, x, X.start, dir='+')
                if L.is_finite is not True or L.has(AccumBounds):
                    return False
            if X.end.is_finite and X.right_open:
                L = limit(f, x, X.end, dir='-')
                if L.is_finite is not True or L.has(AccumBounds):
                    return False
            # Compact intervals are uniformly continuous
            if not X.left_open and not X.right_open and X.start.is_finite and X.end.is_finite:
                return True
                
        # For unbounded domains, check if the derivative is bounded at infinity
        df = diff(f, x)
        if hasattr(X, 'sup') and X.sup == oo:
            L = limit(df, x, oo)
            if L.is_finite is not True:
                return False
        if hasattr(X, 'inf') and X.inf == -oo:
            L = limit(df, x, -oo)
            if L.is_finite is not True:
                return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness can be a sympy expression `f` (assuming X = Reals) or a tuple `(f, X)`.
    """
    if isinstance(witness, tuple) and len(witness) == 2:
        f, X = witness
    else:
        f = witness
        X = S.Reals
        
    try:
        h1 = bool(is_uniformly_continuous(f, X))
    except Exception:
        h1 = False
        
    try:
        # The conclusion Q is that |f| is uniformly continuous.
        # We want neg_Q to be True when Q fails.
        q = bool(is_uniformly_continuous(Abs(f), X))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is uniformly continuous on X",
    "¬Q: |f| is not uniformly continuous on X"
]

N_HYP = 1
NEG_Q_INDEX = 1