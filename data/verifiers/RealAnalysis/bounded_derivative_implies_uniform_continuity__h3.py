import sympy
from sympy import Symbol, Interval, S, limit, Abs, degree, singularities, AccumBounds, Reals, oo, sin, cos, exp, log, sqrt, pi
import sympy.abc as abc

# Top-level setup for witness expressions
x = Symbol('x', real=True)

def is_interval(I):
    return isinstance(I, Interval) or I == S.Reals or I == Reals

def is_differentiable_on(f, x_sym, I):
    try:
        df = f.diff(x_sym)
        
        # Check endpoints if they are included in the interval
        if hasattr(I, 'inf') and I.inf in I:
            val = df.subs(x_sym, I.inf)
            if val.is_infinite or val.is_real == False or val == S.NaN:
                return False
        if hasattr(I, 'sup') and I.sup in I:
            val = df.subs(x_sym, I.sup)
            if val.is_infinite or val.is_real == False or val == S.NaN:
                return False
                    
        # Check for singularities of the derivative in the interval
        try:
            sing_df = singularities(df, x_sym)
            if hasattr(sing_df, 'intersect'):
                inter = sing_df.intersect(I)
                if hasattr(inter, 'is_empty') and inter.is_empty == False:
                    return False
        except Exception:
            pass
                
        # Check for singularities of the function itself in the interval
        try:
            sing_f = singularities(f, x_sym)
            if hasattr(sing_f, 'intersect'):
                inter = sing_f.intersect(I)
                if hasattr(inter, 'is_empty') and inter.is_empty == False:
                    return False
        except Exception:
            pass
                
        return True
    except Exception:
        return False

def is_uniformly_continuous(f, x_sym, I):
    try:
        inf = I.inf if hasattr(I, 'inf') else S.NegativeInfinity
        sup = I.sup if hasattr(I, 'sup') else S.Infinity
        
        # For any open finite endpoints, the limit must exist and be finite
        for ep in [inf, sup]:
            if ep not in [S.NegativeInfinity, S.Infinity] and ep not in I:
                dir = '+' if ep == inf else '-'
                L = limit(f, x_sym, ep, dir=dir)
                if isinstance(L, AccumBounds) or L.is_infinite or L == S.NaN or L.has(S.Infinity, S.NegativeInfinity, S.ComplexInfinity):
                    return False
                    
        is_bnd = I.is_bounded if hasattr(I, 'is_bounded') else False
        
        # For unbounded intervals, check behavior at infinity
        if not is_bnd:
            df = f.diff(x_sym)
            if sup == S.Infinity:
                L = limit(Abs(df), x_sym, S.Infinity)
                if L == S.Infinity:
                    return False
            if inf == S.NegativeInfinity:
                L = limit(Abs(df), x_sym, S.NegativeInfinity)
                if L == S.Infinity:
                    return False
            
            # Polynomials of degree >= 2 are not uniformly continuous on unbounded intervals
            if f.is_polynomial(x_sym):
                if degree(f, x_sym) >= 2:
                    return False
                return True
            
            # Numerical heuristic for oscillating or other unbounded derivative cases
            diffs = []
            for n in [10, 100, 1000, 10000]:
                c1 = I.contains(n)
                c2 = I.contains(n + 1.0/n)
                if c1 in (True, S.true) and c2 in (True, S.true):
                    val1 = f.subs(x_sym, n).evalf()
                    val2 = f.subs(x_sym, n + 1.0/n).evalf()
                    diffs.append(abs(val1 - val2))
            
            # If the difference |f(x) - f(y)| remains large while |x - y| -> 0
            if len(diffs) >= 3 and all(d > 0.01 for d in diffs):
                return False
                
        return True
    except Exception:
        return True

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        I, f = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_interval(I)
    except Exception:
        h1 = False
        
    try:
        f = sympy.sympify(f)
        syms = list(f.free_symbols)
        if len(syms) > 0:
            x_sym = syms[0]
        else:
            x_sym = Symbol('x', real=True)
    except Exception:
        x_sym = Symbol('x', real=True)
        
    try:
        h2 = is_differentiable_on(f, x_sym, I)
    except Exception:
        h2 = False
        
    try:
        unif_cont = is_uniformly_continuous(f, x_sym, I)
        neg_q = not unif_cont
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is an interval",
    "H_2: f is differentiable on I",
    "¬Q: f is not uniformly continuous on I"
]

N_HYP = 2
NEG_Q_INDEX = 2