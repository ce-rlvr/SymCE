import sympy
from sympy import Symbol, limit, oo, Abs, Max, S
from sympy.calculus.util import maximum

# Top-level setup
# (No specific named objects required for this Real Analysis conjecture)

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: (f_n) converges uniformly to f on X",
    "¬Q: f_n^+ does not converge uniformly to f^+ on X"
]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_n = witness['f_n']
            f = witness['f']
            X = witness['X']
            x = witness.get('x', Symbol('x', real=True))
            n = witness.get('n', Symbol('n', integer=True, positive=True))
            x_n = witness.get('x_n', None)
        else:
            f_n, f, X, x, n = witness
            x_n = None
            
        if isinstance(X, tuple):
            X = sympy.Interval(X[0], X[1])
    except Exception:
        return [False, False]

    # H1: f_n converges uniformly to f on X
    h1_ok = False
    try:
        diff = Abs(f_n - f)
        sup = maximum(diff, x, X)
        lim = limit(sup, n, oo)
        if not isinstance(lim, sympy.Limit) and lim == 0:
            h1_ok = True
    except Exception:
        pass

    # neg_Q: f_n^+ does NOT converge uniformly to f^+ on X
    neg_q_ok = False
    try:
        f_n_plus = Max(f_n, 0)
        f_plus = Max(f, 0)
        diff_plus = Abs(f_n_plus - f_plus)
        
        if x_n is not None:
            diff_plus_xn = diff_plus.subs(x, x_n)
            lim_xn = limit(diff_plus_xn, n, oo)
            if not isinstance(lim_xn, sympy.Limit) and lim_xn != 0:
                neg_q_ok = True
        
        if not neg_q_ok:
            try:
                sup_plus = maximum(diff_plus, x, X)
                lim_plus = limit(sup_plus, n, oo)
                if not isinstance(lim_plus, sympy.Limit) and lim_plus != 0:
                    neg_q_ok = True
            except Exception:
                pass
                
        if not neg_q_ok:
            # Fallback using alternative definition of positive part
            f_n_plus_alt = (f_n + Abs(f_n)) / 2
            f_plus_alt = (f + Abs(f)) / 2
            diff_plus_alt = Abs(f_n_plus_alt - f_plus_alt)
            sup_plus_alt = maximum(diff_plus_alt, x, X)
            lim_plus_alt = limit(sup_plus_alt, n, oo)
            if not isinstance(lim_plus_alt, sympy.Limit) and lim_plus_alt != 0:
                neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, neg_q_ok]