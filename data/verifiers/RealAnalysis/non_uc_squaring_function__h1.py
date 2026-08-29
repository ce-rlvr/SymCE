import sympy
from sympy import Symbol, S
from sympy.calculus.util import maximum, continuous_domain

x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    neg_q = False
    try:
        if callable(witness):
            try:
                witness = witness(x)
            except Exception:
                pass
        
        f = sympy.sympify(witness)
        free_syms = getattr(f, "free_symbols", None)
        
        if free_syms is None:
            return [False]
            
        if len(free_syms) == 0:
            neg_q = True
        elif len(free_syms) == 1:
            sym = list(free_syms)[0]
            
            try:
                domain = continuous_domain(f, sym, S.Reals)
                if domain != S.Reals:
                    return [False]
            except Exception:
                pass
            
            if f.is_polynomial(sym):
                deg = sympy.degree(f, sym)
                if deg <= 1:
                    neg_q = True
            else:
                df = sympy.diff(f, sym)
                if df.is_constant():
                    neg_q = True
                else:
                    try:
                        max_val = maximum(abs(df), sym, S.Reals)
                        if max_val.is_finite:
                            neg_q = True
                    except Exception:
                        pass
    except Exception:
        pass

    return [neg_q]

CONDITION_LABELS = ["¬Q: f is uniformly continuous on R"]
N_HYP = 0
NEG_Q_INDEX = 0