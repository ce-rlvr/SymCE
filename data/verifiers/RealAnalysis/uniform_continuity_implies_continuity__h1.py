import sympy as sp
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: f is uniformly continuous on X",
    "¬Q: f is not continuous at every point in X"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f', witness)
            domain = witness.get('domain', sp.S.Reals)
        else:
            f = witness
            domain = sp.S.Reals
            
        f = sp.sympify(f)
        
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        else:
            var = x
            
        try:
            cont_domain = sp.calculus.util.continuous_domain(f, var, domain)
            is_continuous = (cont_domain == domain)
        except Exception:
            is_continuous = False
            
        neg_q = not is_continuous
        
        if not is_continuous:
            h1 = False
        else:
            if getattr(domain, 'is_bounded', False) and getattr(domain, 'is_closed', False):
                h1 = True
            else:
                try:
                    df = sp.diff(f, var)
                    frange = sp.calculus.util.function_range(df, var, domain)
                    if getattr(frange, 'is_bounded', False):
                        h1 = True
                    elif f.is_polynomial(var):
                        h1 = sp.degree(f, var) <= 1
                    else:
                        h1 = False
                except Exception:
                    h1 = False
                    
    except Exception:
        h1 = False
        neg_q = False
        
    return [bool(h1), bool(neg_q)]