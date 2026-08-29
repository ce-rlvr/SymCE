import math
from sympy.ntheory import n_order

# Top-level setup
# No named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        m, n, a = witness
    except Exception:
        return [False, False, False]

    try:
        m_val = int(m)
        n_val = int(n)
        h1 = (m_val == m) and (n_val == n) and (m_val > 1) and (n_val > 1)
    except Exception:
        h1 = False

    try:
        a_val = int(a)
        h2 = (a_val == a) and (math.gcd(a_val, m_val * n_val) == 1)
    except Exception:
        h2 = False

    try:
        ord_mn = n_order(a_val, m_val * n_val)
        ord_m = n_order(a_val, m_val)
        ord_n = n_order(a_val, n_val)
        lcm_ord = (ord_m * ord_n) // math.gcd(ord_m, ord_n)
        neg_q = bool(ord_mn != lcm_ord)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are integers greater than 1",
    "H_2: a is an integer coprime to mn",
    "¬Q: The order of a modulo mn is not equal to lcm(ord_m(a), ord_n(a))"
]

N_HYP = 2
NEG_Q_INDEX = 2