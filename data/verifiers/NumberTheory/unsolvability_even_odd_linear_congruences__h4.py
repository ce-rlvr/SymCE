import sympy
import math

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        a_raw, b_raw, m_raw = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = True
        for x in (a_raw, b_raw, m_raw):
            if not isinstance(x, (int, sympy.Integer)):
                h1 = False
        a = int(a_raw)
        b = int(b_raw)
        m = int(m_raw)
    except Exception:
        h1 = False

    try:
        h2 = h1 and m > 0 and m % 2 == 0
    except Exception:
        h2 = False

    try:
        h3 = h1 and a % 2 == 0
    except Exception:
        h3 = False

    try:
        if h1 and m > 0:
            g = math.gcd(a, m)
            neg_q = (b % g == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, m are integers",
    "H_2: m is an even positive integer",
    "H_3: a is an even integer",
    "¬Q: The linear congruence ax ≡ b (mod m) has an integer solution"
]

N_HYP = 3
NEG_Q_INDEX = 3