import sympy

x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        f, a, b, y = witness
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        y = sympy.sympify(y)
        
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = sympy.sympify(f)
            
        h1 = False
        if a.is_number and b.is_number and y.is_number and a.is_real and b.is_real and y.is_real:
            if bool(a.evalf() <= b.evalf()):
                free_syms = list(f_expr.free_symbols)
                if len(free_syms) == 1:
                    f_expr = f_expr.subs(free_syms[0], x)
                    h1 = True
                elif len(free_syms) == 0:
                    h1 = True
                
                if h1:
                    mid = (a + b) / 2
                    val = f_expr.subs(x, mid).evalf()
                    if val.is_number and val.is_real is False:
                        h1 = False
    except Exception:
        h1 = False

    try:
        if h1:
            dom = sympy.calculus.util.continuous_domain(f_expr, x, sympy.Interval(a, b))
            h2 = (dom == sympy.Interval(a, b))
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            sols = sympy.solveset(f_expr - y, x, domain=sympy.Interval(a, b))
            if sols == sympy.EmptySet:
                neg_q = True
            elif isinstance(sols, sympy.ConditionSet):
                m = sympy.calculus.util.minimum(f_expr, x, sympy.Interval(a, b)).evalf()
                M = sympy.calculus.util.maximum(f_expr, x, sympy.Interval(a, b)).evalf()
                y_val = y.evalf()
                if bool(y_val < m) or bool(y_val > M):
                    neg_q = True
                else:
                    neg_q = False
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on the closed interval a to b",
    "H_2: f is continuous at every point in the interval",
    "¬Q: There is no point c in the interval such that f(c) = y"
]

N_HYP = 2
NEG_Q_INDEX = 2