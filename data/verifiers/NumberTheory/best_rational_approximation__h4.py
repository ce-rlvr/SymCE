import sympy
import sympy.ntheory
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# No specific named groups needed for this number theory problem.

CONDITION_LABELS = [
    "H_1: x is an irrational number",
    "H_2: n is a non-negative integer",
    "H_3: p and q are integers",
    "H_4: (p, q) is not equal to (p_n, q_n)",
    "¬Q: |q_n x - p_n| >= |q x - p|"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x_val = witness['x']
            n_val = witness['n']
            p_val = witness['p']
            q_val = witness['q']
        else:
            x_val, n_val, p_val, q_val = witness
    except Exception:
        return [False] * 5

    try:
        x_sym = sympy.sympify(x_val)
        h1 = x_sym.is_irrational is True
    except Exception:
        h1 = False

    try:
        n_sym = sympy.sympify(n_val)
        h2 = n_sym.is_integer and bool(n_sym >= 0)
    except Exception:
        h2 = False

    try:
        p_sym = sympy.sympify(p_val)
        q_sym = sympy.sympify(q_val)
        h3 = p_sym.is_integer and q_sym.is_integer
    except Exception:
        h3 = False

    p_n, q_n = None, None
    try:
        if h2:
            it = sympy.ntheory.continued_fraction_iterator(x_sym)
            p_minus_1, q_minus_1 = 1, 0
            p_minus_2, q_minus_2 = 0, 1
            
            for i in range(int(n_sym) + 1):
                a = next(it)
                p_curr = a * p_minus_1 + p_minus_2
                q_curr = a * q_minus_1 + q_minus_2
                p_minus_2, q_minus_2 = p_minus_1, q_minus_1
                p_minus_1, q_minus_1 = p_curr, q_curr
                
            p_n, q_n = p_curr, q_curr
    except Exception:
        pass

    try:
        if p_n is not None and q_n is not None and h3:
            h4 = bool((p_sym != p_n) or (q_sym != q_n))
        else:
            h4 = False
    except Exception:
        h4 = False

    try:
        if p_n is not None and q_n is not None and h3:
            if p_sym == -p_n and q_sym == -q_n:
                neg_q = True
            else:
                lhs = abs(q_n * x_sym - p_n)
                rhs = abs(q_sym * x_sym - p_sym)
                diff = (lhs - rhs).evalf(200)
                neg_q = bool(diff >= 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]