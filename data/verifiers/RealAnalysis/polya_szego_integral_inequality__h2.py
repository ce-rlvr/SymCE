import sympy as sp
import sympy.abc
import math

x = sympy.abc.x

def conditions(witness):
    try:
        f_expr = witness['f']
        g_expr = witness['g']
        a = float(witness['a'])
        b = float(witness['b'])
        m1 = float(witness['m1'])
        M1 = float(witness['M1'])
        m2 = float(witness['m2'])
        M2 = float(witness['M2'])
    except Exception:
        return [False, False, False]

    if callable(f_expr):
        f_func = f_expr
    else:
        try:
            f_func = sp.lambdify(x, f_expr, modules=['math'])
        except Exception:
            return [False, False, False]

    if callable(g_expr):
        g_func = g_expr
    else:
        try:
            g_func = sp.lambdify(x, g_expr, modules=['math'])
        except Exception:
            return [False, False, False]

    try:
        h1 = (a < b)
        float(f_func((a + b) / 2))
        float(g_func((a + b) / 2))
    except Exception:
        h1 = False

    try:
        h2 = True
        if m2 <= 0:
            h2 = False
        else:
            N = 100
            for i in range(N + 1):
                xi = a + i * (b - a) / N
                g_val = float(g_func(xi))
                if not (m2 - 1e-7 <= g_val <= M2 + 1e-7):
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        if m1 <= 0 or M1 <= 0 or m2 <= 0 or M2 <= 0:
            neg_q = False
        else:
            def simpson(func, a, b, n=10000):
                h = (b - a) / n
                s = func(a) + func(b)
                s_odd = sum(func(a + i * h) for i in range(1, n, 2))
                s_even = sum(func(a + i * h) for i in range(2, n - 1, 2))
                return (s + 4 * s_odd + 2 * s_even) * h / 3

            int_f2 = simpson(lambda t: float(f_func(t))**2, a, b)
            int_g2 = simpson(lambda t: float(g_func(t))**2, a, b)
            int_fg = simpson(lambda t: float(f_func(t)) * float(g_func(t)), a, b)

            if int_fg == 0:
                lhs = float('inf')
            else:
                lhs = (int_f2 * int_g2) / (int_fg**2)

            rhs = ((M1 * M2 + m1 * m2)**2) / (4 * m1 * m2 * M1 * M2)

            neg_q = lhs > rhs + 1e-7
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f and g are Lebesgue measurable functions",
    "H_2: 0 < m_2 <= g(x) <= M_2 for almost every x",
    "not Q: The Polya-Szego inequality fails"
]

N_HYP = 2
NEG_Q_INDEX = 2