import sympy
from sympy import Symbol, Interval, EmptySet
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

def conditions(witness):
    try:
        f, a, b = witness
    except Exception:
        return [False, False]
    
    try:
        a_val = float(a)
        b_val = float(b)
        if not (a_val < b_val):
            h1 = False
        else:
            df = f.diff(x)
            dom_f = continuous_domain(f, x, Interval(a, b))
            dom_df = continuous_domain(df, x, Interval(a, b))
            h1 = (dom_f == Interval(a, b)) and (dom_df == Interval(a, b))
    except Exception:
        h1 = False

    try:
        a_val = float(a)
        b_val = float(b)
        df = f.diff(x)
        eq = df * (x - a) - (f - f.subs(x, a))
        
        if sympy.simplify(eq) == 0:
            neg_q = False
        else:
            sols = sympy.solveset(eq, x, domain=Interval.open(a, b))
            if sols == EmptySet:
                neg_q = True
            elif isinstance(sols, sympy.FiniteSet):
                neg_q = len(sols) == 0
            else:
                roots = sympy.solve(eq, x)
                has_root_in_interval = False
                for r in roots:
                    try:
                        if r.is_real is not False:
                            val = float(r.evalf())
                            if a_val < val < b_val:
                                has_root_in_interval = True
                                break
                    except Exception:
                        pass
                
                if not has_root_in_interval:
                    n_points = 100
                    step = (b_val - a_val) / n_points
                    prev_val = None
                    for i in range(1, n_points):
                        pt = a_val + i * step
                        try:
                            val = float(eq.subs(x, pt).evalf())
                            if prev_val is not None:
                                if prev_val * val <= 0:
                                    has_root_in_interval = True
                                    break
                            prev_val = val
                        except Exception:
                            pass
                
                neg_q = not has_root_in_interval
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is differentiable on the closed interval a to b",
    "¬Q: no c in the open interval a to b satisfies df(c) = (f(c) - f(a)) / (c - a)"
]

N_HYP = 1
NEG_Q_INDEX = 1