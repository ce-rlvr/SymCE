import sympy as sp
from sympy.calculus.util import continuous_domain

# Top-level setup
x = sp.Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: limit as x -> oo of f(x) exists and is a finite real number",
    "¬Q: f is NOT uniformly continuous on [a, oo)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Witness can be a tuple (f, a) or just f (with default a=0)
        if isinstance(witness, tuple):
            f, a = witness
        else:
            f = witness
            a = 0
            
        f = sp.sympify(f)
        a = sp.sympify(a)
            
        symbols = list(f.free_symbols)
        if len(symbols) == 1:
            sym = symbols[0]
        elif len(symbols) == 0:
            sym = x
        else:
            syms = [s for s in symbols if s.name == 'x']
            if syms:
                sym = syms[0]
            else:
                sym = symbols[0]
    except Exception:
        return [False, False]
        
    # H_1: limit as x -> oo of f(x) exists and is a finite real number
    try:
        L = sp.limit(f, sym, sp.oo)
        h1 = bool(L.is_real and L.is_finite)
    except Exception:
        h1 = False
        
    # ¬Q: f is NOT uniformly continuous on [a, oo)
    try:
        dom = continuous_domain(f, sym, sp.Interval(a, sp.oo))
        is_continuous = (dom == sp.Interval(a, sp.oo))
        
        if not is_continuous:
            # If it's not continuous on [a, oo), it cannot be uniformly continuous
            neg_q = True
        else:
            # If it is continuous on [a, oo) and has a finite limit at infinity,
            # then by the continuous extension theorem, it IS uniformly continuous.
            L_for_q = sp.limit(f, sym, sp.oo)
            if L_for_q.is_real and L_for_q.is_finite:
                neg_q = False
            else:
                # Fallback heuristic for functions that do not satisfy H_1
                df = f.diff(sym)
                L_df = sp.limit(df, sym, sp.oo)
                if L_df == sp.oo or L_df == -sp.oo or L_df == sp.zoo:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]