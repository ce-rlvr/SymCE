import sympy
import math
from sympy import Symbol

x = Symbol('x')

def eval_func(func, val):
    if isinstance(func, (int, float)):
        return float(func)
    if hasattr(func, 'subs'):
        return float(func.subs(x, val))
    else:
        return float(func(val))

def eval_fg(f, g, val):
    return eval_func(f, val) * eval_func(g, val)

def simpson(func, a, b, n=200):
    if a == b:
        return 0.0
    if n % 2 == 1:
        n += 1
    h = float(b - a) / n
    s = eval_func(func, a) + eval_func(func, b)
    for i in range(1, n, 2):
        s += 4 * eval_func(func, a + i * h)
    for i in range(2, n - 1, 2):
        s += 2 * eval_func(func, a + i * h)
    return s * h / 3.0

def simpson_fg(f, g, a, b, n=200):
    if a == b:
        return 0.0
    if n % 2 == 1:
        n += 1
    h = float(b - a) / n
    s = eval_fg(f, g, a) + eval_fg(f, g, b)
    for i in range(1, n, 2):
        s += 4 * eval_fg(f, g, a + i * h)
    for i in range(2, n - 1, 2):
        s += 2 * eval_fg(f, g, a + i * h)
    return s * h / 3.0

def conditions(witness):
    try:
        f, g, a_raw, b_raw = witness
        a = float(a_raw)
        b = float(b_raw)
    except Exception:
        return [False, False, False]
    
    try:
        h1 = True
        a_min, b_max = min(a, b), max(a, b)
        if a_min < b_max:
            n_points = 200
            step = float(b_max - a_min) / n_points
            prev_val = eval_func(f, a_min)
            for i in range(1, n_points + 1):
                val = eval_func(f, a_min + i * step)
                if val > prev_val + 1e-7:
                    h1 = False
                    break
                prev_val = val
    except Exception:
        h1 = False

    try:
        h2 = True
        a_min, b_max = min(a, b), max(a, b)
        if a_min == b_max:
            val = eval_func(g, a_min)
            if not (-1e-7 <= val <= 1 + 1e-7):
                h2 = False
        else:
            n_points = 200
            step = float(b_max - a_min) / n_points
            for i in range(n_points + 1):
                val = eval_func(g, a_min + i * step)
                if not (-1e-7 <= val <= 1 + 1e-7):
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        c_val = simpson(g, a, b, 200)
        left_val = simpson(f, b - c_val, b, 200)
        mid_val = simpson_fg(f, g, a, b, 200)
        right_val = simpson(f, a, a + c_val, 200)
        
        neg_q = (left_val > mid_val + 1e-5) or (mid_val > right_val + 1e-5)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The function f is non-increasing on the interval",
    "H_2: 0 <= g(x) <= 1 for all x in the interval",
    "¬Q: The conclusion fails"
]

N_HYP = 2
NEG_Q_INDEX = 2