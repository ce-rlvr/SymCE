import sympy
import math

r = sympy.Symbol('r', real=True, positive=True)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x_val = witness.get('x')
            if hasattr(x_val, '__iter__'):
                default_n = len(list(x_val))
            else:
                default_n = 1
            n = witness.get('n', default_n)
            g = witness.get('g', r**2)
            x = x_val
        elif isinstance(witness, (list, tuple)) and len(witness) == 3 and isinstance(witness[0], int) and hasattr(witness[2], '__iter__'):
            n, g, x = witness
        elif hasattr(witness, '__iter__'):
            x = list(witness)
            n = len(x)
            g = r**2
        else:
            x = [witness]
            n = 1
            g = r**2
            
        if hasattr(x, '__iter__'):
            x = list(x)
        else:
            x = [x]
            
        g = sympy.sympify(g)
    except Exception:
        return [False, False, False]

    # H1: g is a differentiable function on (0, \infty)
    try:
        if not hasattr(g, 'diff'):
            h1 = False
        else:
            dg = sympy.diff(g, r)
            h1 = True
    except Exception:
        h1 = False

    # H2: f is defined by f(x) = g(||x||) on R^n \ {0}
    try:
        if isinstance(n, int) and n >= 1 and len(x) == n:
            all_nums = True
            for xi in x:
                try:
                    float(xi)
                except Exception:
                    all_nums = False
                    break
            h2 = all_nums
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The conclusion fails.
    try:
        norm_x_sq = sum(xi**2 for xi in x)
        if norm_x_sq == 0:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: g is a differentiable function on (0, infinity)",
    "H_2: f is defined by f(x) = g(||x||) on R^n \\ {0}",
    "¬Q: f is not differentiable at x, or its gradient does not match the formula"
]

N_HYP = 2
NEG_Q_INDEX = 2