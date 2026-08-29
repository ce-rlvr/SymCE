import sympy
from sympy import Interval, S, limit, diff, AccumBounds
from sympy.calculus.util import continuous_domain

# Top-level setup
x = sympy.Symbol('x', real=True)

def is_interval(I):
    if I == S.Reals:
        return True
    if isinstance(I, Interval):
        return True
    return False

def is_NOT_uniformly_continuous(f, I, var):
    # 1. Check if f is continuous on I
    try:
        dom = continuous_domain(f, var, I)
        if not I.is_subset(dom):
            return True
    except Exception:
        pass
        
    # 2. Check limits at finite endpoints not in I
    for ep in [I.inf, I.sup]:
        if ep.is_finite and ep not in I:
            try:
                lim = limit(f, var, ep, dir='+' if ep == I.inf else '-')
                if not lim.is_finite or isinstance(lim, AccumBounds):
                    return True
            except Exception:
                pass
                
    # 3. Check behavior at infinity
    try:
        df = diff(f, var)
        for ep in [I.inf, I.sup]:
            if not ep.is_finite:
                # If limit of df is oo or -oo, it implies f grows faster than linearly
                # or has unbounded derivative in a way that prevents uniform continuity
                lim_df = limit(df, var, ep)
                if lim_df == S.Infinity or lim_df == S.NegativeInfinity:
                    return True
                
                # If limit of f/x is oo or -oo, f grows faster than linearly
                lim_fx = limit(f/var, var, ep)
                if lim_fx == S.Infinity or lim_fx == S.NegativeInfinity:
                    return True
    except Exception:
        pass

    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            I = witness.get('I')
            f = witness.get('f')
        else:
            I, f = witness
    except Exception:
        return [False, False]
        
    # H1: I is an interval in the real numbers
    try:
        h1 = is_interval(I)
    except Exception:
        h1 = False
        
    # neg_Q: f is not uniformly continuous on I
    try:
        f_sym = sympy.sympify(f)
        syms = f_sym.free_symbols
        if len(syms) == 1:
            var = list(syms)[0]
        elif len(syms) == 0:
            var = x
        else:
            if x in syms:
                var = x
            else:
                var = list(syms)[0]
                
        neg_q = is_NOT_uniformly_continuous(f_sym, I, var)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is an interval in the real numbers",
    "¬Q: f is not uniformly continuous on I"
]

N_HYP = 1
NEG_Q_INDEX = 1