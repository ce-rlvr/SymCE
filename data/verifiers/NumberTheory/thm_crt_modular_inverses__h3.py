import math
import sympy
from sympy import Rational, Integer

# No specific named bindings needed for Number Theory

def conditions(witness) -> list[bool]:
    try:
        m, n, a, x = witness
    except Exception:
        return [False] * 5 + [False]

    # H1: m and n are positive integers
    try:
        m_int = int(m)
        n_int = int(n)
        h1 = (m_int == m) and (n_int == n) and m_int > 0 and n_int > 0
    except Exception:
        h1 = False

    # H2: \gcd(m, n) = 1
    try:
        h2 = math.gcd(int(m), int(n)) == 1
    except Exception:
        h2 = False

    # H3: \gcd(a, m n) = 1
    try:
        h3 = math.gcd(int(a), int(m) * int(n)) == 1
    except Exception:
        h3 = False

    # H4: x \equiv a^{-1} \pmod m
    try:
        inv_m = pow(int(a), -1, int(m))
        h4 = (x - inv_m) % int(m) == 0
    except Exception:
        h4 = False

    # H5: x \equiv a^{-1} \pmod n
    try:
        inv_n = pow(int(a), -1, int(n))
        h5 = (x - inv_n) % int(n) == 0
    except Exception:
        h5 = False

    # ¬Q: x \not\equiv a^{-1} \pmod{m n}
    try:
        inv_mn = pow(int(a), -1, int(m) * int(n))
        q = (x - inv_mn) % (int(m) * int(n)) == 0
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    r"H_1: m and n are positive integers",
    r"H_2: \gcd(m, n) = 1",
    r"H_3: \gcd(a, m n) = 1",
    r"H_4: x \equiv a^{-1} \pmod m",
    r"H_5: x \equiv a^{-1} \pmod n",
    r"¬Q: x \not\equiv a^{-1} \pmod{m n}"
]

N_HYP = 5
NEG_Q_INDEX = 5