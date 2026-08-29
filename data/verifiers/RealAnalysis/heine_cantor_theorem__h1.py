import sympy
from sympy import Symbol, Interval, oo, S, Limit, Union, FiniteSet

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    The witness is expected to be a tuple: (domain, f)
    where `domain` is a sympy.Set and `f` is a sympy.Expr in terms of `x`.
    """
    try:
        domain, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: X is a compact metric space
    # In R, a set is compact if and only if it is closed and bounded.
    try:
        h1 = bool(domain.is_closed) and bool(domain.is_bounded)
    except Exception:
        h1 = False
        
    # H_2: f is a continuous function on X
    try:
        from sympy.calculus.util import continuous_domain
        cd = continuous_domain(f, x, domain)
        h2 = bool(domain.is_subset(cd))
    except Exception:
        h2 = False
        
    # ¬Q: f is NOT uniformly continuous on X
    try:
        def check_uniformly_continuous(f, domain):
            if not h2:
                return False
            
            intervals = domain.args if isinstance(domain, sympy.Union) else [domain]
            df = sympy.diff(f, x)
            
            for iv in intervals:
                if not isinstance(iv, sympy.Interval):
                    continue
                
                # Check finite endpoints: limit must be finite for uniform continuity
                if iv.start != -sympy.oo and iv.left_open:
                    L = sympy.limit(f, x, iv.start, dir='+')
                    if L.is_finite is False:
                        return False
                if iv.end != sympy.oo and iv.right_open:
                    L = sympy.limit(f, x, iv.end, dir='-')
                    if L.is_finite is False:
                        return False
                
                # Check infinite endpoints: if function limit is not finite, derivative must be bounded
                if iv.end == sympy.oo:
                    Lf = sympy.limit(f, x, sympy.oo)
                    if Lf.is_finite is not True:
                        Ldf = sympy.limit(df, x, sympy.oo)
                        if Ldf.is_finite is False:
                            return False
                if iv.start == -sympy.oo:
                    Lf = sympy.limit(f, x, -sympy.oo)
                    if Lf.is_finite is not True:
                        Ldf = sympy.limit(df, x, -sympy.oo)
                        if Ldf.is_finite is False:
                            return False
                            
            return True
            
        neg_q = not check_uniformly_continuous(f, domain)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: f is a continuous function",
    "¬Q: f is not uniformly continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2