import sympy
from sympy.ntheory import isprime, multiplicity

# Top-level setup
# No specific named bindings needed for Number Theory.

def conditions(witness) -> list[bool]:
    try:
        p, x, y, n = witness
    except Exception:
        return [False] * 6
    
    try:
        h1 = bool(isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    try:
        h2 = bool(isinstance(x, (int, sympy.Integer)) and isinstance(y, (int, sympy.Integer)))
    except Exception:
        h2 = False

    try:
        h3 = bool(isinstance(n, (int, sympy.Integer)) and n > 0)
    except Exception:
        h3 = False

    try:
        h4 = bool(x % p != 0)
    except Exception:
        h4 = False

    try:
        h5 = bool(y % p != 0)
    except Exception:
        h5 = False

    try:
        lhs = x**n - y**n
        rhs_base = x - y
        if lhs == 0 and rhs_base == 0:
            neg_q = False
        elif lhs == 0 and rhs_base != 0:
            neg_q = True
        else:
            v_p_lhs = multiplicity(p, lhs)
            v_p_x_y = multiplicity(p, rhs_base)
            v_p_n = multiplicity(p, n)
            neg_q = bool(v_p_lhs != v_p_x_y + v_p_n)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: x and y are integers",
    "H_3: n is a positive integer",
    "H_4: p does not divide x",
    "H_5: p does not divide y",
    "¬Q: v_p(x^n - y^n) != v_p(x - y) + v_p(n)"
]

N_HYP = 5
NEG_Q_INDEX = 5