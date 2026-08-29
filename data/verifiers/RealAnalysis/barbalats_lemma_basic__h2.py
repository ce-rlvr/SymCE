import sympy
from sympy import Symbol, oo, limit, diff, periodicity
from sympy.calculus.singularities import singularities
from sympy.calculus.util import continuous_domain
from sympy.sets.sets import Interval

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False
    
    try:
        f = sympy.sympify(witness)
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            f = f.subs(list(free_syms)[0], x)
        elif len(free_syms) > 1:
            for sym in free_syms:
                if sym.name == 'x':
                    f = f.subs(sym, x)
    except Exception:
        return [False, False]

    # H1: f is uniformly continuous on [0, infinity)
    try:
        is_continuous = True
        try:
            dom = continuous_domain(f, x, Interval(0, oo))
            if dom != Interval(0, oo):
                is_continuous = False
        except Exception:
            try:
                sings = singularities(f, x, Interval(0, oo))
                if sings and sings != sympy.EmptySet:
                    is_continuous = False
            except Exception:
                pass
                
        if is_continuous:
            df = diff(f, x)
            is_uc = False
            skip_heuristic = False
            
            if df.is_constant():
                is_uc = True
                skip_heuristic = True
            else:
                try:
                    if periodicity(df, x) is not None:
                        is_uc = True
                        skip_heuristic = True
                except Exception:
                    pass
                    
                if not is_uc:
                    try:
                        L = limit(df, x, oo)
                        if L.is_real:
                            is_uc = True
                            skip_heuristic = True
                        elif L == oo or L == -oo:
                            is_uc = False
                            skip_heuristic = True
                    except Exception:
                        pass
                        
                if not is_uc and not skip_heuristic:
                    max_val = 0
                    # Evaluate derivative at various points to catch unbounded growth
                    test_points = list(range(100)) + [1000 + i for i in range(20)] + [10**k for k in range(4, 8)]
                    for i in test_points:
                        try:
                            val = abs(float(df.subs(x, i)))
                            if val > max_val:
                                max_val = val
                            if max_val > 1000:
                                is_uc = False
                                break
                        except Exception:
                            pass
                    else:
                        # If derivative didn't blow up at test points, assume it's bounded
                        is_uc = True
            h1_ok = is_uc
    except Exception:
        h1_ok = False

    # neg_Q: limit of f(x) as x -> oo is NOT 0
    try:
        L = limit(f, x, oo)
        if L == 0:
            neg_q_ok = False
        else:
            neg_q_ok = True
    except Exception:
        # Fallback if limit cannot be computed symbolically
        try:
            vals = [abs(float(f.subs(x, 10**k))) for k in range(2, 6)]
            if all(v < 1e-5 for v in vals):
                neg_q_ok = False
            else:
                neg_q_ok = True
        except Exception:
            neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is uniformly continuous on [0, infinity)",
    "¬Q: The limit of f(x) as x approaches infinity is not 0"
]

N_HYP = 1
NEG_Q_INDEX = 1