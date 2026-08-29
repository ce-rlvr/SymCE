import sympy
from sympy import Symbol, Interval, S, limit, oo, Abs, FiniteSet
from sympy.calculus.util import continuous_domain, maximum

# Top-level setup
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: (f_n) is a sequence of continuous functions from X to R",
    "H_3: For every convergent sequence x_n -> x in X, the sequence f_n(x_n) converges to f(x)",
    "¬Q: The sequence (f_n) does not converge uniformly to f on X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    x_sym = x
    n_sym = n
    X_obj = None
    f_n_obj = None
    f_obj = None
    
    if isinstance(witness, dict):
        X_obj = witness.get('X')
        f_n_obj = witness.get('f_n')
        f_obj = witness.get('f')
        x_sym = witness.get('x', x_sym)
        n_sym = witness.get('n', n_sym)
    elif isinstance(witness, tuple) and len(witness) >= 3:
        X_obj = witness[0]
        f_n_obj = witness[1]
        f_obj = witness[2]
        if len(witness) >= 5:
            x_sym = witness[3]
            n_sym = witness[4]
    else:
        X_obj = getattr(witness, 'X', None)
        f_n_obj = getattr(witness, 'f_n', None)
        f_obj = getattr(witness, 'f', None)
        x_sym = getattr(witness, 'x', x_sym)
        n_sym = getattr(witness, 'n', n_sym)

    # H1: X is a compact metric space
    H1 = False
    try:
        if isinstance(X_obj, Interval):
            H1 = X_obj.is_closed and X_obj.is_bounded
        elif isinstance(X_obj, FiniteSet):
            H1 = True
        elif hasattr(X_obj, 'is_closed') and hasattr(X_obj, 'is_bounded'):
            H1 = X_obj.is_closed and X_obj.is_bounded
    except Exception:
        pass

    def get_val(expr, x_val, n_val=None):
        if callable(expr):
            if n_val is not None:
                return float(expr(n_val, x_val))
            return float(expr(x_val))
        if n_val is not None:
            return float(expr.subs({x_sym: x_val, n_sym: n_val}))
        return float(expr.subs({x_sym: x_val}))

    def check_continuous_fn(expr, domain_set, is_seq=False):
        try:
            if not callable(expr):
                domain = continuous_domain(expr, x_sym, S.Reals)
                if domain_set.is_subset(domain):
                    return True
        except Exception:
            pass
        try:
            if isinstance(domain_set, Interval):
                a = float(domain_set.start)
                b = float(domain_set.end)
                if a == float('-inf'): a = -100.0
                if b == float('inf'): b = 100.0
                n_val = 10
                for i in range(100):
                    x_val = a + (b - a) * i / 100.0
                    x_next = x_val + 1e-5
                    val1 = get_val(expr, x_val, n_val) if is_seq else get_val(expr, x_val)
                    val2 = get_val(expr, x_next, n_val) if is_seq else get_val(expr, x_next)
                    if abs(val1 - val2) > 0.1:
                        return False
                return True
            elif isinstance(domain_set, FiniteSet):
                return True
        except Exception:
            pass
        return False

    # H2: (f_n) is a sequence of continuous functions from X to R
    H2 = False
    if X_obj is not None and f_n_obj is not None:
        H2 = check_continuous_fn(f_n_obj, X_obj, is_seq=True)

    # Check if f is continuous
    f_continuous = False
    if X_obj is not None and f_obj is not None:
        f_continuous = check_continuous_fn(f_obj, X_obj, is_seq=False)

    def check_unif(domain_set):
        try:
            if not callable(f_n_obj) and not callable(f_obj):
                diff = Abs(f_n_obj - f_obj)
                max_val = maximum(diff, x_sym, domain_set)
                lim_max = limit(max_val, n_sym, oo)
                if lim_max == 0:
                    return True
                return False
        except Exception:
            pass
            
        try:
            if isinstance(domain_set, FiniteSet):
                for n_val in [100, 500, 1000]:
                    max_diff = 0
                    for x_val in domain_set:
                        val = abs(get_val(f_n_obj, x_val, n_val) - get_val(f_obj, x_val))
                        if val > max_diff:
                            max_diff = val
                    if max_diff > 0.1:
                        return False
                return True
            elif isinstance(domain_set, Interval):
                a = float(domain_set.start)
                b = float(domain_set.end)
                if a == float('-inf'): a = -1000.0
                if b == float('inf'): b = 1000.0
                for n_val in [100, 500, 1000]:
                    max_diff = 0
                    for i in range(101):
                        x_val = a + (b - a) * i / 100.0
                        val = abs(get_val(f_n_obj, x_val, n_val) - get_val(f_obj, x_val))
                        if val > max_diff:
                            max_diff = val
                    if max_diff > 0.1:
                        return False
                return True
            return False
        except Exception:
            return False

    is_unif_X = False
    if X_obj is not None and f_n_obj is not None and f_obj is not None:
        is_unif_X = check_unif(X_obj)

    # H3: Continuous convergence
    H3 = False
    try:
        if X_obj is not None and f_n_obj is not None and f_obj is not None:
            if H1:
                H3 = is_unif_X and f_continuous
            else:
                if isinstance(X_obj, Interval):
                    a = float(X_obj.start)
                    b = float(X_obj.end)
                    if a == float('-inf'): a = -100.0
                    if b == float('inf'): b = 100.0
                    margin = (b - a) * 0.1
                    sub_X = Interval(a + margin, b - margin)
                    H3 = check_unif(sub_X) and f_continuous
                elif isinstance(X_obj, FiniteSet):
                    H3 = is_unif_X and f_continuous
    except Exception:
        pass

    # neg_Q: The sequence (f_n) does NOT converge uniformly to f on X
    neg_Q = False
    if X_obj is not None and f_n_obj is not None and f_obj is not None:
        neg_Q = not is_unif_X

    return [H1, H2, H3, neg_Q]