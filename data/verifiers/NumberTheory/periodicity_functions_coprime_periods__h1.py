import math
import sympy
from sympy.abc import x

# Top-level setup
# No specific named bindings required for this number theory conjecture.

def evaluate(f, val):
    """Helper to evaluate a function, sympy expression, or subscriptable object at a given integer."""
    if callable(f):
        return f(val)
    elif hasattr(f, 'free_symbols'):
        symbols = list(f.free_symbols)
        if len(symbols) == 1:
            return f.subs(symbols[0], val)
        elif len(symbols) == 0:
            return f
        else:
            return f.subs(x, val)
    elif isinstance(f, dict):
        return f[val]
    else:
        return f[val]

def conditions(witness) -> list[bool]:
    try:
        a, b, f = witness
    except Exception:
        return [False] * 5

    # H_1: a and b are positive integers
    try:
        h1 = (isinstance(a, (int, sympy.Integer)) and not isinstance(a, bool) and 
              isinstance(b, (int, sympy.Integer)) and not isinstance(b, bool) and 
              a > 0 and b > 0)
    except Exception:
        h1 = False

    # H_2: gcd(a, b) = 1
    try:
        h2 = math.gcd(int(a), int(b)) == 1
    except Exception:
        h2 = False

    # H_3: f(x + a) = f(x) for all integers x
    try:
        a_int = int(a)
        h3 = all(evaluate(f, i + a_int) == evaluate(f, i) for i in range(-200, 201))
    except Exception:
        h3 = False

    # H_4: f(x + b) = f(x) for all integers x
    try:
        b_int = int(b)
        h4 = all(evaluate(f, i + b_int) == evaluate(f, i) for i in range(-200, 201))
    except Exception:
        h4 = False

    # ¬Q: f(x + 1) != f(x) for some integer x
    try:
        neg_q = not all(evaluate(f, i + 1) == evaluate(f, i) for i in range(-200, 201))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are positive integers",
    "H_2: gcd(a, b) = 1",
    "H_3: f(x + a) = f(x) for all integers x",
    "H_4: f(x + b) = f(x) for all integers x",
    "¬Q: f(x + 1) != f(x) for some integer x"
]

N_HYP = 4
NEG_Q_INDEX = 4