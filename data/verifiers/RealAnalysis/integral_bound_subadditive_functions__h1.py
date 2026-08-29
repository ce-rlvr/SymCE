import sympy as sp
import math

t, x = sp.symbols('t x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f_input, x_val = witness
        else:
            f_input = witness
            x_val = -1.0
    except Exception:
        return [False, False, False]

    try:
        x_float = float(x_val)
    except Exception:
        return [False, False, False]

    try:
        if isinstance(f_input, sp.Expr):
            symbols = list(f_input.free_symbols)
            if len(symbols) == 1:
                t_sym = symbols[0]
            else:
                t_sym = sp.Symbol('t')
            f = sp.lambdify(t_sym, f_input, 'math')
        elif isinstance(f_input, (int, float)):
            val = float(f_input)
            f = lambda _: val
        else:
            f = f_input
            
        _ = float(f(0))
        _ = float(f(x_float))
        
        N = 10000
        if x_float == 0:
            integral_val = 0.0
        else:
            dx = x_float / N
            integral_val = sum(f(i * dx + dx/2) for i in range(N)) * dx
    except Exception:
        return [False, False, False]

    try:
        h1 = math.isfinite(integral_val) and x_float >= 0
    except Exception:
        h1 = False

    try:
        h2 = True
        if x_float >= 0:
            N_grid = 100
            dx_grid = x_float / N_grid
            for i in range(N_grid + 1):
                for j in range(N_grid + 1 - i):
                    s = i * dx_grid
                    t_val = j * dx_grid
                    if f(s + t_val) > f(s) + f(t_val) + 1e-5:
                        h2 = False
                        break
                if not h2:
                    break
        else:
            h2 = True
    except Exception:
        h2 = False

    try:
        fx = float(f(x_float))
        rhs = (x_float / 2.0) * fx
        neg_q = integral_val < rhs - 1e-5
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued Riemann integrable function on the interval from 0 to x",
    "H_2: f(s+t) <= f(s) + f(t) for all s, t >= 0 such that s+t <= x",
    "¬Q: integral of f(t) from 0 to x < x/2 * f(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2