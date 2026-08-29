import sympy as sp

x = sp.Symbol('x', real=True)

def get_min_max(f_expr, a, b):
    vals = []
    try:
        vals.append(float(f_expr.subs(x, a)))
        vals.append(float(f_expr.subs(x, b)))
    except Exception:
        pass
        
    try:
        df = sp.diff(f_expr, x)
        crit_points = sp.solveset(df, x, domain=sp.Interval(a, b))
        if crit_points != sp.S.EmptySet:
            if isinstance(crit_points, sp.FiniteSet):
                for cp in crit_points:
                    try:
                        vals.append(float(f_expr.subs(x, cp)))
                    except Exception:
                        pass
    except Exception:
        pass
        
    if not vals:
        return None, None
    return min(vals), max(vals)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
        else:
            f, a, b = witness
            
        a_sym = sp.sympify(a)
        b_sym = sp.sympify(b)
        
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = sp.sympify(f)
            
        a_val = float(a_sym)
        b_val = float(b_sym)
        
        if a_val >= b_val:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    h1 = False
    try:
        is_cont = False
        try:
            sings = sp.singularities(f_expr, x)
            if sings.intersect(sp.Interval(a_sym, b_sym)) == sp.S.EmptySet:
                is_cont = True
        except Exception:
            if f_expr.has(sp.Piecewise):
                is_cont = False
            elif f_expr.is_polynomial(x):
                is_cont = True
            else:
                is_cont = True
                
        if is_cont:
            min_val, max_val = get_min_max(f_expr, a_sym, b_sym)
            if min_val is not None and min_val >= a_val - 1e-9 and max_val <= b_val + 1e-9:
                h1 = True
    except Exception:
        h1 = False

    h2 = False
    try:
        val_a = f_expr.subs(x, a_sym)
        if sp.simplify(val_a - b_sym) == 0:
            h2 = True
        elif abs(float(val_a) - b_val) < 1e-9:
            h2 = True
    except Exception:
        h2 = False

    neg_q = False
    try:
        roots = sp.solveset(f_expr - x, x, domain=sp.Interval.open(a_sym, b_sym))
        if roots is sp.S.EmptySet:
            neg_q = True
        elif isinstance(roots, sp.FiniteSet):
            neg_q = len(roots) == 0
        else:
            min_diff, max_diff = get_min_max(f_expr - x, a_sym, b_sym)
            if min_diff is not None and (min_diff > 1e-9 or max_diff < -1e-9):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a continuous function from a to b",
    "H_2: f(a) = b",
    "¬Q: There is no point c between a and b such that f(c) = c"
]

N_HYP = 2
NEG_Q_INDEX = 2