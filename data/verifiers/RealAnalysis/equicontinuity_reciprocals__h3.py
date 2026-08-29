import sympy
from sympy import Symbol, Limit, S, Interval
from sympy.calculus.singularities import singularities

# Top-level setup for witness expressions
x = Symbol('x', real=True)

def is_uniformly_continuous(f, domain):
    """
    Checks if a sympy expression f is uniformly continuous on the given sympy Interval.
    This is a heuristic check sufficient for standard counterexamples.
    """
    if not hasattr(domain, 'is_Interval') or not domain.is_Interval:
        return False
        
    free_syms = f.free_symbols
    if len(free_syms) > 1:
        return False
    elif len(free_syms) == 1:
        sym = list(free_syms)[0]
    else:
        sym = Symbol('x', real=True)
        
    # Check limits at endpoints
    if domain.start != S.NegativeInfinity:
        L_start = Limit(f, sym, domain.start, dir='+').doit()
        if getattr(L_start, 'is_finite', None) is not True:
            return False
    else:
        L_start = Limit(f, sym, S.NegativeInfinity).doit()
        if getattr(L_start, 'is_finite', None) is not True:
            df = f.diff(sym)
            L_df = Limit(df, sym, S.NegativeInfinity).doit()
            if getattr(L_df, 'is_finite', None) is not True:
                return False

    if domain.end != S.Infinity:
        L_end = Limit(f, sym, domain.end, dir='-').doit()
        if getattr(L_end, 'is_finite', None) is not True:
            return False
    else:
        L_end = Limit(f, sym, S.Infinity).doit()
        if getattr(L_end, 'is_finite', None) is not True:
            df = f.diff(sym)
            L_df = Limit(df, sym, S.Infinity).doit()
            if getattr(L_df, 'is_finite', None) is not True:
                return False

    # Check for singularities inside the domain
    try:
        sing = singularities(f, sym)
        intersect = sing.intersect(domain)
        if getattr(intersect, 'is_empty', None) == False:
            return False
    except Exception:
        pass

    return True

def conditions(witness) -> list[bool]:
    X = None
    F = None
    R = None
    
    if isinstance(witness, dict):
        X = witness.get('X')
        F = witness.get('F')
        R = witness.get('R')
    elif isinstance(witness, tuple) and len(witness) >= 2:
        X = witness[0]
        F = witness[1]
        R = witness[2] if len(witness) > 2 else None
    else:
        return [False, False, False, False]
        
    # H1: X is a metric space
    try:
        if X == S.Reals:
            X = Interval(S.NegativeInfinity, S.Infinity)
        h1 = hasattr(X, 'is_Interval') and X.is_Interval
    except Exception:
        h1 = False
        
    # H2: F is an equicontinuous family of real-valued functions on X
    try:
        h2 = False
        if isinstance(F, list) and len(F) > 0:
            h2 = True
            for f in F:
                if not is_uniformly_continuous(f, X):
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # H3: R is the family of functions defined by g(x) = 1/f(x) for each f in F
    try:
        h3 = False
        if h1 and isinstance(F, list) and len(F) > 0:
            h3 = True
            # Check that f(x) != 0 on X so that 1/f(x) is well-defined
            for f in F:
                free_syms = f.free_symbols
                sym = list(free_syms)[0] if len(free_syms) == 1 else x
                zeros = sympy.solveset(f, sym, domain=X)
                if getattr(zeros, 'is_empty', None) == False:
                    h3 = False
                    break
            
            if h3:
                if R is not None:
                    if len(R) == len(F):
                        for r, f in zip(R, F):
                            if sympy.simplify(r - 1/f) != 0:
                                h3 = False
                                break
                    else:
                        h3 = False
                else:
                    R = [1/f for f in F]
    except Exception:
        h3 = False
        
    # neg_Q: R is NOT equicontinuous on X
    try:
        neg_q = False
        if h3 and R is not None:
            for r in R:
                if not is_uniformly_continuous(r, X):
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: F is an equicontinuous family of real-valued functions on X",
    "H_3: R is the family of functions defined by g(x) = 1/f(x) for each f in F",
    "¬Q: R is not equicontinuous on X"
]

N_HYP = 3
NEG_Q_INDEX = 3