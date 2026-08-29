import sympy
import math

def conditions(witness):
    try:
        a, b, c, m = witness
    except Exception:
        return [False, False, False, False]

    try:
        m_sym = sympy.sympify(m)
        h1 = bool(m_sym.is_integer) and bool(m_sym > 0)
    except Exception:
        h1 = False

    try:
        diff = sympy.sympify(a) - sympy.sympify(b)
        quotient = sympy.simplify(diff / m_sym)
        h2 = quotient.is_integer is False
    except Exception:
        h2 = False

    try:
        c_sym = sympy.sympify(c)
        h3 = sympy.gcd(c_sym, m_sym) == 1
    except Exception:
        h3 = False

    try:
        diff_c = sympy.sympify(a) * c_sym - sympy.sympify(b) * c_sym
        quotient_c = sympy.simplify(diff_c / m_sym)
        neg_q = quotient_c.is_integer is True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: a \\not\\equiv b \\pmod m",
    "H_3: gcd(c, m) = 1",
    "¬Q: ac \\equiv bc \\pmod m"
]

N_HYP = 3
NEG_Q_INDEX = 3