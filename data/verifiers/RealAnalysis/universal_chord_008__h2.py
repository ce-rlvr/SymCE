import sympy
from sympy.calculus.util import continuous_domain, minimum, maximum
import math

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should be a dictionary or tuple providing (f, a, b, n).
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            a = witness.get('a')
            b = witness.get('b')
            n = witness.get('n')
        else:
            f, a, b, n = witness
            
        if callable(f):
            f = f(x)
        elif isinstance(f, str):
            f = sympy.sympify(f, locals={'x': x})
        elif isinstance(f, sympy.Expr):
            free_syms = list(f.free_symbols)
            if len(free_syms) == 1 and free_syms[0] != x:
                f = f.subs(free_syms[0], x)
        else:
            f = sympy.sympify(f)
                
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        n = sympy.sympify(n)
    except Exception:
        return [False, False, False]

    # H_1: f is a real-valued function continuous on the closed interval a to b
    try:
        if a >= b:
            h1_ok = False
        else:
            domain = continuous_domain(f, x, sympy.Interval(a, b))
            h1_ok = bool(sympy.Interval(a, b).is_subset(domain))
    except Exception:
        h1_ok = False

    # H_2: n is a positive integer
    try:
        h2_ok = bool(n.is_integer and n > 0)
    except Exception:
        h2_ok = False

    # ¬Q: There does NOT exist a point c in a to b - (b-a)/n such that f(c) = f(c + (b-a)/n)
    try:
        if not h2_ok or a >= b:
            neg_q_ok = False
        else:
            shift = (b - a) / n
            g = sympy.simplify(f.subs(x, x + shift) - f)
            interval = sympy.Interval(a, b - shift)
            
            if g.is_constant():
                val = float(g)
                neg_q_ok = abs(val) > 1e-9
            else:
                try:
                    roots = sympy.solveset(g, x, domain=interval)
                    if roots is sympy.S.EmptySet:
                        neg_q_ok = True
                    elif isinstance(roots, sympy.FiniteSet) and len(roots) > 0:
                        neg_q_ok = False
                    elif roots == interval:
                        neg_q_ok = False
                    else:
                        raise ValueError("Complex root set")
                except Exception:
                    try:
                        min_val = float(minimum(g, x, interval))
                        max_val = float(maximum(g, x, interval))
                        if min_val > 1e-7 or max_val < -1e-7:
                            neg_q_ok = True
                        else:
                            neg_q_ok = False
                    except Exception:
                        # Grid evaluation fallback
                        N_grid = 1000
                        vals = []
                        for i in range(N_grid + 1):
                            pt = a + i * (b - shift - a) / N_grid
                            vals.append(float(g.subs(x, pt)))
                        if max(vals) < -1e-5 or min(vals) > 1e-5:
                            neg_q_ok = True
                        else:
                            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a real-valued function continuous on the closed interval from a to b",
    "H_2: n is a positive integer",
    "¬Q: There does NOT exist a point c in the interval from a to b - (b-a)/n such that f(c) = f(c + (b-a)/n)"
]

N_HYP = 2
NEG_Q_INDEX = 2