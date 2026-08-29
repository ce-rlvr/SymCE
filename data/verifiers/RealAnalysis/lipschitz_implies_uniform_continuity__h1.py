import sympy
from sympy import Symbol, S, oo, Abs, limit, AccumBounds, zoo
from sympy.calculus.util import continuous_domain, maximum, minimum

CONDITION_LABELS = [
    "H_1: f is a Lipschitz continuous function",
    "¬Q: f is not uniformly continuous on X"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            f, domain = witness
        else:
            f = witness
            domain = S.Reals
            
        f = sympy.sympify(f)
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            x = list(free_syms)[0]
        elif len(free_syms) == 0:
            x = Symbol('x', real=True)
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H1: f is Lipschitz continuous
    h1 = False
    try:
        df = f.diff(x)
        max_df = maximum(df, x, domain)
        min_df = minimum(df, x, domain)
        if max_df < oo and min_df > -oo:
            h1 = True
    except Exception:
        h1 = False

    # neg_Q: f is not uniformly continuous
    neg_q = False
    try:
        if h1:
            # Lipschitz continuity implies uniform continuity
            neg_q = False
        else:
            is_compact = domain.is_Interval and not domain.left_open and not domain.right_open and domain.start.is_finite and domain.end.is_finite
            if is_compact:
                cd = continuous_domain(f, x, domain)
                if domain.is_subset(cd):
                    neg_q = False
                else:
                    neg_q = True
            else:
                try:
                    cd = continuous_domain(f, x, domain)
                    if not domain.is_subset(cd):
                        neg_q = True
                except Exception:
                    pass

                if not neg_q and domain.is_Interval:
                    if domain.left_open and domain.start.is_finite:
                        L = limit(f, x, domain.start, dir='+')
                        if L in [oo, -oo, zoo] or isinstance(L, AccumBounds):
                            neg_q = True
                    if domain.right_open and domain.end.is_finite:
                        L = limit(f, x, domain.end, dir='-')
                        if L in [oo, -oo, zoo] or isinstance(L, AccumBounds):
                            neg_q = True
                
                if not neg_q:
                    superlinear = False
                    if hasattr(domain, 'sup') and domain.sup == oo:
                        L = limit(f/x, x, oo)
                        if L in [oo, -oo, zoo]:
                            superlinear = True
                    if hasattr(domain, 'inf') and domain.inf == -oo:
                        L = limit(f/x, x, -oo)
                        if L in [oo, -oo, zoo]:
                            superlinear = True
                    
                    if superlinear:
                        neg_q = True
                    else:
                        unbounded_df_at_inf = False
                        if hasattr(domain, 'sup') and domain.sup == oo:
                            try:
                                L_df = limit(Abs(df), x, oo)
                                if L_df == oo or (hasattr(L_df, 'sup') and L_df.sup == oo):
                                    unbounded_df_at_inf = True
                            except Exception:
                                pass
                        if hasattr(domain, 'inf') and domain.inf == -oo:
                            try:
                                L_df = limit(Abs(df), x, -oo)
                                if L_df == oo or (hasattr(L_df, 'sup') and L_df.sup == oo):
                                    unbounded_df_at_inf = True
                            except Exception:
                                pass
                        
                        if unbounded_df_at_inf:
                            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]