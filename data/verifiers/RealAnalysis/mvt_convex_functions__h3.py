import sympy
from sympy import Symbol, limit, nsimplify, Abs, exp, log, sin, cos, pi, Rational, Integer
import math

x = Symbol('x')

def conditions(witness):
    """
    witness is expected to be a dict with keys:
      'f': sympy expression for f(x)
      'I': tuple (lower, upper) for the interval
      'a': real number
      'b': real number
    Alternatively, a tuple (f, I, a, b).
    """
    try:
        if isinstance(witness, dict):
            f_expr = witness['f']
            I = witness['I']
            a = witness['a']
            b = witness['b']
        else:
            f_expr, I, a, b = witness
    except Exception:
        return [False, False, False, False]

    try:
        f_expr = sympy.sympify(f_expr)
        free_syms = f_expr.free_symbols
        if len(free_syms) == 1:
            x_sym = list(free_syms)[0]
        else:
            x_sym = Symbol('x')
    except Exception:
        return [False, False, False, False]

    # H1: I is an open interval and a, b in I
    try:
        lower, upper = I
        l_val = float(lower)
        u_val = float(upper)
        a_val = float(a)
        b_val = float(b)
        h1 = (l_val < u_val) and (l_val < a_val < u_val) and (l_val < b_val < u_val)
    except Exception:
        h1 = False

    # H2: f is convex on I
    try:
        l = l_val if l_val != -float('inf') else min(-100.0, a_val - 10.0, b_val - 10.0)
        u = u_val if u_val != float('inf') else max(100.0, a_val + 10.0, b_val + 10.0)
        points = [l + (u - l) * i / 10.0 for i in range(1, 10)]
        h2 = True
        for i in range(len(points)):
            for j in range(i, len(points)):
                x1 = points[i]
                x2 = points[j]
                for k in range(1, 5):
                    t = k / 5.0
                    xt = t * x1 + (1 - t) * x2
                    
                    val1 = float(f_expr.subs(x_sym, x1))
                    val2 = float(f_expr.subs(x_sym, x2))
                    valt = float(f_expr.subs(x_sym, xt))
                    
                    if valt > t * val1 + (1 - t) * val2 + 1e-5:
                        h2 = False
                        break
                if not h2: break
            if not h2: break
    except Exception:
        h2 = False

    # H3: f'_+ and f'_- denote right and left derivatives
    h3 = True

    # neg_Q: conclusion fails
    try:
        if float(a) == float(b):
            neg_q = True
        else:
            a_sym = nsimplify(a)
            b_sym = nsimplify(b)
            h_sym = Symbol('h', positive=True)
            
            diff_plus = limit((f_expr.subs(x_sym, a_sym+h_sym) - f_expr.subs(x_sym, a_sym))/h_sym, h_sym, 0)
            diff_minus = limit((f_expr.subs(x_sym, b_sym) - f_expr.subs(x_sym, b_sym-h_sym))/h_sym, h_sym, 0)
            
            fraction = (f_expr.subs(x_sym, b_sym) - f_expr.subs(x_sym, a_sym)) / (b_sym - a_sym)
            
            c1 = float(diff_plus) <= float(fraction) + 1e-7
            c2 = float(fraction) <= float(diff_minus) + 1e-7
            neg_q = not (c1 and c2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: I is an open interval and a, b in I",
    "H_2: f is a convex function on I",
    "H_3: f'_+ and f'_- denote the right and left derivatives of f",
    "¬Q: The inequality f'_+(a) <= (f(b)-f(a))/(b-a) <= f'_-(b) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3