import sympy as sp
from sympy import Symbol, S, Interval, limit, oo, Abs, diff, calculus

# Top-level setup
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

CONDITION_LABELS = [
    "H_1: f: X \\to Y is uniformly continuous",
    "H_2: (x_n) is a Cauchy sequence in X",
    "¬Q: (f(x_n)) is not a Cauchy sequence in Y"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_finite_limit(L):
    if L.has(sp.oo, -sp.oo, sp.zoo, sp.AccumBounds):
        return False
    if L.is_finite:
        return True
    if L.is_number:
        return True
    return False

def check_cauchy(expr, n_sym):
    try:
        L = limit(expr, n_sym, oo)
        return is_finite_limit(L)
    except Exception:
        return False

def _check_uc_base(f_expr, x_sym, domain):
    try:
        if isinstance(domain, Interval):
            left_lim = limit(f_expr, x_sym, domain.start, dir='+')
            right_lim = limit(f_expr, x_sym, domain.end, dir='-')
            if is_finite_limit(left_lim) and is_finite_limit(right_lim):
                sings = calculus.singularities(f_expr, x_sym, domain)
                if sings.is_empty:
                    return True
                    
        df = diff(f_expr, x_sym)
        if df.is_constant():
            return True
            
        try:
            max_val = calculus.util.maximum(Abs(df), x_sym, domain)
            if is_finite_limit(max_val):
                return True
        except Exception:
            pass
    except Exception:
        pass
    return False

def check_uniformly_continuous(f_expr, x_sym, domain):
    try:
        if isinstance(domain, Interval):
            if domain == S.Reals:
                d1 = Interval(-oo, -1)
                d2 = Interval(-1, 1)
                d3 = Interval(1, oo)
                if _check_uc_base(f_expr, x_sym, d1) and \
                   _check_uc_base(f_expr, x_sym, d2) and \
                   _check_uc_base(f_expr, x_sym, d3):
                    return True
            elif domain.end == oo and domain.start.is_finite:
                d1 = Interval(domain.start, domain.start + 1)
                d2 = Interval(domain.start + 1, oo)
                if _check_uc_base(f_expr, x_sym, d1) and \
                   _check_uc_base(f_expr, x_sym, d2):
                    return True
            elif domain.start == -oo and domain.end.is_finite:
                d1 = Interval(-oo, domain.end - 1)
                d2 = Interval(domain.end - 1, domain.end)
                if _check_uc_base(f_expr, x_sym, d1) and \
                   _check_uc_base(f_expr, x_sym, d2):
                    return True
                    
        return _check_uc_base(f_expr, x_sym, domain)
    except Exception:
        pass
    return False

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    try:
        if hasattr(witness, 'is_uniformly_continuous'):
            h1 = bool(witness.is_uniformly_continuous())
            h2 = bool(witness.is_cauchy_sequence())
            neg_q = not bool(witness.is_image_cauchy_sequence())
            return [h1, h2, neg_q]
    except Exception:
        pass

    if isinstance(witness, dict):
        if 'f_is_uniformly_continuous' in witness:
            try:
                h1 = bool(witness['f_is_uniformly_continuous'])
                h2 = bool(witness['x_n_is_cauchy'])
                neg_q = not bool(witness['f_x_n_is_cauchy'])
                return [h1, h2, neg_q]
            except Exception:
                pass

    f_expr = None
    x_n_expr = None
    domain = S.Reals
    x_sym = x
    n_sym = n
    
    if isinstance(witness, dict):
        f_expr = witness.get('f')
        x_n_expr = witness.get('x_n')
        x_sym = witness.get('x', x)
        n_sym = witness.get('n', n)
        domain = witness.get('domain', domain)
    elif isinstance(witness, tuple) and len(witness) >= 2:
        f_expr = witness[0]
        x_n_expr = witness[1]
        if len(witness) >= 3:
            domain = witness[2]
            
    if f_expr is not None and x_n_expr is not None:
        try:
            if callable(f_expr):
                f_sym = f_expr(x_sym)
            else:
                f_sym = f_expr
        except Exception:
            f_sym = None
            
        try:
            if callable(x_n_expr):
                x_n_sym = x_n_expr(n_sym)
            else:
                x_n_sym = x_n_expr
        except Exception:
            x_n_sym = None

        if f_sym is not None and x_n_sym is not None:
            try:
                h1 = check_uniformly_continuous(f_sym, x_sym, domain)
            except Exception:
                h1 = False
                
            try:
                h2 = check_cauchy(x_n_sym, n_sym)
            except Exception:
                h2 = False
                
            try:
                if callable(f_expr):
                    f_x_n = f_expr(x_n_sym)
                else:
                    f_x_n = f_sym.subs(x_sym, x_n_sym)
                neg_q = not check_cauchy(f_x_n, n_sym)
            except Exception:
                neg_q = False

    return [h1, h2, neg_q]