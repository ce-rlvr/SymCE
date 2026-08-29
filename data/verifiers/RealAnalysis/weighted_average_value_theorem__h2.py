import sympy
from sympy.abc import x

def conditions(witness):
    """
    witness is expected to be a tuple: (f, a, b, W, X)
    where:
      - f is a sympy expression in terms of x
      - a and b are the real endpoints of the interval a to b
      - W is a list of weights w_1, ..., w_n
      - X is a list of points x_1, ..., x_n
    """
    try:
        f, a, b, W, X = witness
    except Exception:
        return [False, False, False]

    # H_1: f is a continuous function on the closed interval a to b
    try:
        f_sym = sympy.sympify(f)
        if float(a) >= float(b):
            h1 = False
        else:
            if f_sym.is_polynomial(x):
                h1 = True
            else:
                from sympy.calculus.util import continuous_domain
                dom = continuous_domain(f_sym, x, sympy.Interval(a, b))
                h1 = sympy.Interval(a, b).is_subset(dom)
    except Exception:
        h1 = False

    # H_2: w_1, w_2, ..., w_n are strictly positive real numbers
    try:
        h2 = len(W) > 0 and len(W) == len(X) and all(float(w) > 0 for w in W)
    except Exception:
        h2 = False

    # ¬Q: There is no point c in the interval such that f(c) is the weighted average
    try:
        f_sym = sympy.sympify(f)
        num = sum(float(w) * float(f_sym.subs(x, xi)) for w, xi in zip(W, X))
        den = sum(float(w) for w in W)
        V = num / den
        
        points_to_check = [float(a), float(b)]
        n_samples = 1000
        for i in range(1, n_samples):
            pt = float(a) + (float(b) - float(a)) * i / n_samples
            points_to_check.append(pt)
            
        try:
            df = sympy.diff(f_sym, x)
            crit_points = sympy.solveset(df, x, domain=sympy.Interval(a, b))
            if isinstance(crit_points, sympy.FiniteSet):
                for cp in crit_points:
                    if cp.is_real:
                        points_to_check.append(float(cp))
        except Exception:
            pass

        vals = [float(f_sym.subs(x, p)) for p in points_to_check]
        min_val = min(vals)
        max_val = max(vals)
        
        # The conclusion holds if V is within the range of f on the interval.
        # The negated conclusion holds if V is strictly outside this range.
        tol = 1e-7
        neg_q = (V < min_val - tol) or (V > max_val + tol)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuous function on the closed interval a to b",
    "H_2: w_1 to w_n are strictly positive real numbers",
    "¬Q: There is no point c in the interval such that f(c) is the weighted average"
]

N_HYP = 2
NEG_Q_INDEX = 2