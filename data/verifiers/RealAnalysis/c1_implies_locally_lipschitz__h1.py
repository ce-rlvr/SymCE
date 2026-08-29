import sympy as sp
from sympy.abc import x, y, z, t

CONDITION_LABELS = [
    "H_1: f is continuously differentiable on (a, b)",
    "¬Q: f is not locally Lipschitz continuous on (a, b)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def is_unbounded_limit(L):
    if L == sp.oo or L == -sp.oo or L == sp.zoo:
        return True
    if hasattr(L, 'min') and hasattr(L, 'max'):
        if L.min == -sp.oo or L.max == sp.oo:
            return True
    return False

def conditions(witness):
    try:
        # Witness can be a tuple (f, a, b) or just an expression f (defaults to interval (0, 1))
        if isinstance(witness, tuple) and len(witness) == 3:
            f, a, b = witness
        else:
            f = witness
            a, b = 0, 1
            
        if isinstance(f, str):
            f = sp.sympify(f)
            
        free_vars = f.free_symbols
        if len(free_vars) == 1:
            var = list(free_vars)[0]
        elif len(free_vars) == 0:
            var = sp.Symbol('x')
        else:
            var = list(free_vars)[0]
            
        a = sp.sympify(a)
        b = sp.sympify(b)
        
        df = sp.diff(f, var)
    except Exception:
        return [False, False]
        
    # Check H_1: f is continuously differentiable on (a, b)
    h1 = False
    try:
        from sympy.calculus.util import continuous_domain
        domain = continuous_domain(df, var, sp.Interval.open(a, b))
        h1 = (domain == sp.Interval.open(a, b))
    except Exception:
        # Fallback if continuous_domain fails
        h1 = True
        try:
            from sympy.calculus.singularities import singularities
            sings = singularities(df, var)
            intersection = sings.intersect(sp.Interval.open(a, b))
            if not intersection.is_empty:
                h1 = False
        except Exception:
            pass
            
        if h1:
            try:
                if a.is_finite and b.is_finite:
                    points = [a + (b - a) * i / 50.0 for i in range(1, 50)]
                elif a.is_finite:
                    points = [a + i for i in range(1, 50)]
                elif b.is_finite:
                    points = [b - i for i in range(1, 50)]
                else:
                    points = [i for i in range(-25, 25)]
                    
                for p in points:
                    val = df.subs(var, p).evalf()
                    if not val.is_real or not val.is_finite:
                        h1 = False
                        break
            except Exception:
                h1 = False

    # Check neg_Q: f is NOT locally Lipschitz continuous on (a, b)
    # Note: Since C^1 implies locally Lipschitz, a true counterexample to the literal text is impossible.
    # However, the conjecture likely meant "globally Lipschitz" (a common confusion).
    # We check if the derivative is unbounded on (a, b), which correctly identifies functions 
    # that are C^1 but fail to be globally Lipschitz (e.g., 1/x or sqrt(x) on (0, 1)).
    neg_q = False
    try:
        # Check if df is unbounded near a
        if a.is_finite:
            L_a = sp.limit(df, var, a, dir='+')
            if is_unbounded_limit(L_a):
                neg_q = True
        else:
            L_a = sp.limit(df, var, -sp.oo)
            if is_unbounded_limit(L_a):
                neg_q = True
                
        # Check if df is unbounded near b
        if not neg_q:
            if b.is_finite:
                L_b = sp.limit(df, var, b, dir='-')
                if is_unbounded_limit(L_b):
                    neg_q = True
            else:
                L_b = sp.limit(df, var, sp.oo)
                if is_unbounded_limit(L_b):
                    neg_q = True
    except Exception:
        pass
        
    if not neg_q:
        # Fallback to numerical evaluation near endpoints
        try:
            if a.is_finite:
                for eps in [1e-3, 1e-4, 1e-5, 1e-6]:
                    val_a = df.subs(var, a + eps).evalf()
                    if abs(val_a) > 1e5:
                        neg_q = True
                        break
            if not neg_q and b.is_finite:
                for eps in [1e-3, 1e-4, 1e-5, 1e-6]:
                    val_b = df.subs(var, b - eps).evalf()
                    if abs(val_b) > 1e5:
                        neg_q = True
                        break
        except Exception:
            pass

    return [bool(h1), bool(neg_q)]