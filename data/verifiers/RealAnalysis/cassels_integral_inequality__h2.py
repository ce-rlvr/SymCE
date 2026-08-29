import sympy as sp
from sympy.abc import x
import math

def conditions(witness):
    """
    witness is expected to be a dict with keys: 'f', 'g', 'a', 'b', 'm', 'M'
    or a tuple (f, g, a, b, m, M).
    f and g should be sympy expressions.
    """
    try:
        if isinstance(witness, dict):
            f = sp.sympify(witness['f'])
            g = sp.sympify(witness['g'])
            a = float(witness['a'])
            b = float(witness['b'])
            m = float(witness['m'])
            M = float(witness['M'])
        else:
            f, g, a, b, m, M = witness
            f = sp.sympify(f)
            g = sp.sympify(g)
            a = float(a)
            b = float(b)
            m = float(m)
            M = float(M)
    except Exception:
        return [False, False, False]

    try:
        free_symbols = f.free_symbols | g.free_symbols
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        else:
            var = x
    except Exception:
        var = x

    # H1: f and g are continuous, positive functions on the interval
    def check_positive(expr, a, b):
        if a > b:
            return True
        if a == b:
            try:
                return float(expr.subs(var, a)) > 0
            except Exception:
                return False
        for i in range(101):
            val = a + (b - a) * i / 100.0
            try:
                if float(expr.subs(var, val)) <= 0:
                    return False
            except Exception:
                return False
        return True

    try:
        h1 = check_positive(f, a, b) and check_positive(g, a, b)
    except Exception:
        h1 = False

    # H2: There exist real numbers m and M such that 0 < m <= f(x)/g(x) <= M
    def check_bounds(f, g, a, b, m, M):
        if m <= 0:
            return False
        if a > b:
            return True
        if a == b:
            try:
                ratio = float(f.subs(var, a)) / float(g.subs(var, a))
                return m <= ratio <= M
            except Exception:
                return False
        for i in range(101):
            val = a + (b - a) * i / 100.0
            try:
                ratio = float(f.subs(var, val)) / float(g.subs(var, val))
                if not (m <= ratio <= M):
                    return False
            except Exception:
                return False
        return True

    try:
        h2 = check_bounds(f, g, a, b, m, M)
    except Exception:
        h2 = False

    def integrate_simpson(expr, lower, upper, n=1000):
        if lower == upper:
            return 0.0
        dx = (upper - lower) / n
        s = float(expr.subs(var, lower)) + float(expr.subs(var, upper))
        for i in range(1, n):
            val = float(expr.subs(var, lower + i * dx))
            if i % 2 == 0:
                s += 2 * val
            else:
                s += 4 * val
        return s * dx / 3.0

    try:
        if a > b:
            sign = -1
            lower, upper = b, a
        else:
            sign = 1
            lower, upper = a, b
            
        int_f2 = sign * integrate_simpson(f**2, lower, upper)
        int_g2 = sign * integrate_simpson(g**2, lower, upper)
        int_fg = sign * integrate_simpson(f*g, lower, upper)
        
        lhs = (int_f2 * int_g2) / (int_fg**2)
        rhs = ((m + M)**2) / (4 * m * M)
        
        neg_q = lhs > rhs + 1e-9
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: f and g are continuous positive functions", "H_2: There exist real numbers m and M such that 0 < m <= f(x)/g(x) <= M", "not Q: The inequality fails"]

N_HYP = 2
NEG_Q_INDEX = 2