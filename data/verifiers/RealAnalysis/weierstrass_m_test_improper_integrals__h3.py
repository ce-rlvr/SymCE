import sympy
import math
import itertools
import functools

# Top-level setup for the namespace
x, t = sympy.symbols('x t')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys: 'f', 'M', 'a', 'X'.
    """
    try:
        f = sympy.sympify(witness['f'])
        M = sympy.sympify(witness['M'])
        a = sympy.sympify(witness['a'])
        X = witness['X']
    except Exception:
        return [False, False, False, False]
        
    # H_1: f(x, t) is a real-valued function defined for x in X and t in [a, oo)
    h1_ok = False
    try:
        if a.is_real and isinstance(X, sympy.Set):
            if isinstance(X, sympy.Interval):
                if X.start.is_finite and X.end.is_finite:
                    pt_x = X.start + (X.end - X.start)/2
                elif X.start.is_finite:
                    pt_x = X.start + 1
                elif X.end.is_finite:
                    pt_x = X.end - 1
                else:
                    pt_x = 0
            elif isinstance(X, sympy.FiniteSet):
                pt_x = list(X)[0]
            else:
                pt_x = 0
            val = f.subs({x: pt_x, t: a + 1}).evalf()
            if val.is_real:
                h1_ok = True
    except Exception:
        pass

    # H_2: f(x, t) is locally integrable with respect to t on [a, oo) for each fixed x in X
    h2_ok = False
    try:
        if isinstance(X, sympy.Interval):
            if X.start.is_finite and X.end.is_finite:
                pt_x = X.start + (X.end - X.start)/2
            elif X.start.is_finite:
                pt_x = X.start + 1
            elif X.end.is_finite:
                pt_x = X.end - 1
            else:
                pt_x = 0
        elif isinstance(X, sympy.FiniteSet):
            pt_x = list(X)[0]
        else:
            pt_x = 0
        f_pt = f.subs(x, pt_x)
        val = sympy.integrate(f_pt, (t, a, a + 1))
        if not val.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan, sympy.AccumBounds) and val.is_finite is not False:
            h2_ok = True
    except Exception:
        pass

    # H_3: The improper integral of M(t) from a to oo converges
    h3_ok = False
    try:
        val = sympy.integrate(M, (t, a, sympy.oo))
        if not val.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan, sympy.AccumBounds) and val.is_finite is not False:
            h3_ok = True
    except Exception:
        pass

    # neg_Q: The improper integral of f(x, t) from a to oo does NOT converge uniformly on X
    neg_q_ok = False
    try:
        pts = []
        if isinstance(X, sympy.Interval):
            if X.start.is_finite and X.end.is_finite:
                pts.extend([X.start, X.end, X.start + (X.end - X.start)/2])
            elif X.start.is_finite:
                pts.extend([X.start, X.start + 1, X.start + 10])
            elif X.end.is_finite:
                pts.extend([X.end, X.end - 1, X.end - 10])
            else:
                pts.extend([0, 1, -1])
        elif isinstance(X, sympy.FiniteSet):
            pts = list(X)
        else:
            pts = [0, 1, -1]
            
        diverges_pointwise = False
        for pt in pts:
            try:
                f_pt = f.subs(x, pt)
                val = sympy.integrate(f_pt, (t, a, sympy.oo))
                if val.has(sympy.oo, -sympy.oo, sympy.zoo, sympy.nan, sympy.AccumBounds) or val.is_finite is False:
                    diverges_pointwise = True
                    break
            except Exception:
                pass
                
        if diverges_pointwise:
            neg_q_ok = True
        else:
            R = sympy.Symbol('R', real=True, positive=True)
            tail = sympy.integrate(f, (t, R, sympy.oo))
            if not tail.has(sympy.Integral):
                seqs = []
                if isinstance(X, sympy.Interval):
                    if X.start.is_finite:
                        seqs.extend([X.start + 1/R, X.start + 1/sympy.sqrt(R), X.start + 1/(R**2)])
                    if X.end.is_finite:
                        seqs.extend([X.end - 1/R, X.end - 1/sympy.sqrt(R), X.end - 1/(R**2)])
                    if not X.start.is_finite:
                        seqs.extend([-R, -sympy.sqrt(R), -R**2])
                    if not X.end.is_finite:
                        seqs.extend([R, sympy.sqrt(R), R**2])
                else:
                    seqs.extend([1/R, 1/sympy.sqrt(R), R, sympy.sqrt(R)])
                    
                for expr_x in seqs:
                    try:
                        tail_sub = tail.subs(x, expr_x)
                        lim = sympy.limit(tail_sub, R, sympy.oo)
                        if lim == 0:
                            continue
                        if isinstance(lim, sympy.Limit):
                            continue
                        if lim.free_symbols:
                            continue
                        neg_q_ok = True
                        break
                    except Exception:
                        pass
    except Exception:
        pass

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x, t) is a real-valued function defined for x in X and t in [a, oo)",
    "H_2: f(x, t) is locally integrable with respect to t on [a, oo) for each fixed x in X",
    "H_3: The improper integral of M(t) from a to oo converges",
    "¬Q: The improper integral of f(x, t) from a to oo does NOT converge uniformly on X"
]

N_HYP = 3
NEG_Q_INDEX = 3