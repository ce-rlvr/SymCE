import sympy
import math

# Top-level setup
x = sympy.Symbol('x', real=True)

def grid_search_neg_q(f_callable, a, b):
    N = 10000
    grid = [a + i * (b - a) / N for i in range(N + 1)]
    roots = []
    for i in range(N):
        pt1, pt2 = grid[i], grid[i+1]
        try:
            v1, v2 = f_callable(pt1), f_callable(pt2)
            if v1 * v2 <= 0:
                roots.append((pt1 + pt2) / 2.0)
            elif abs(v1) < 1e-5:
                roots.append(pt1)
        except Exception:
            pass
            
    if not roots:
        return True
        
    c = max(roots)
    if c <= a + 1e-5 or c >= b - 1e-5:
        return True
        
    for pt in grid:
        if pt > c + 1e-4:
            try:
                if f_callable(pt) <= 0:
                    return True
            except Exception:
                pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
        else:
            f, a, b = witness
    except Exception:
        return [False, False, False]
        
    if callable(f):
        try:
            f_expr = f(x)
            if isinstance(f_expr, sympy.Expr):
                f = f_expr
        except Exception:
            pass

    # H1: f(a) < 0
    try:
        if isinstance(f, sympy.Expr):
            val_a = float(f.subs(x, a))
        else:
            val_a = float(f(a))
        h1 = bool(val_a < 0)
    except Exception:
        h1 = False

    # H2: f(b) > 0
    try:
        if isinstance(f, sympy.Expr):
            val_b = float(f.subs(x, b))
        else:
            val_b = float(f(b))
        h2 = bool(val_b > 0)
    except Exception:
        h2 = False

    # neg_Q
    neg_q = False
    try:
        if isinstance(f, sympy.Expr):
            try:
                roots = sympy.solveset(f, x, domain=sympy.Interval(a, b))
                if roots.is_empty:
                    neg_q = True
                elif isinstance(roots, sympy.ConditionSet):
                    raise ValueError("ConditionSet")
                else:
                    c = sympy.sup(roots)
                    if c is sympy.S.Infinity or c is sympy.S.NegativeInfinity:
                        neg_q = True
                    else:
                        try:
                            c_float = float(c)
                        except Exception:
                            raise ValueError("Cannot evaluate sup to float")
                            
                        val_c = f.subs(x, c)
                        try:
                            is_root = abs(float(val_c)) < 1e-9
                        except Exception:
                            is_root = sympy.simplify(val_c) == 0
                        
                        if not is_root:
                            neg_q = True
                        elif c_float <= float(a) or c_float >= float(b):
                            neg_q = True
                        else:
                            bad_set = sympy.solveset(f <= 0, x, domain=sympy.Interval.Lopen(c, b))
                            if bad_set.is_empty:
                                neg_q = False
                            elif not isinstance(bad_set, sympy.ConditionSet):
                                neg_q = True
                            else:
                                raise ValueError("ConditionSet")
            except Exception:
                f_callable = lambda val: float(f.subs(x, val))
                neg_q = grid_search_neg_q(f_callable, float(a), float(b))
        elif callable(f):
            f_callable = lambda val: float(f(val))
            neg_q = grid_search_neg_q(f_callable, float(a), float(b))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(a) < 0",
    "H_2: f(b) > 0",
    "¬Q: The set of roots has no maximum c, or f(x) <= 0 for some x > c"
]

N_HYP = 2
NEG_Q_INDEX = 2