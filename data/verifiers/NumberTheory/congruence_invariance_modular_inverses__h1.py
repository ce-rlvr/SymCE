import math
import sympy

CONDITION_LABELS = [
    "H_1: a and b are integers",
    "H_2: gcd(a, m) = 1",
    "H_3: gcd(b, m) = 1",
    "H_4: a == b (mod m)",
    "not Q: a^-1 != b^-1 (mod m)"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False] * 5
        a, b, m = witness
    except Exception:
        return [False] * 5

    # H_1: a and b are integers
    try:
        h1 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer))
    except Exception:
        h1 = False

    # H_2: gcd(a, m) = 1
    try:
        if not isinstance(m, (int, sympy.Integer)):
            h2 = False
        else:
            h2 = math.gcd(int(a), int(m)) == 1
    except Exception:
        h2 = False

    # H_3: gcd(b, m) = 1
    try:
        if not isinstance(m, (int, sympy.Integer)):
            h3 = False
        else:
            h3 = math.gcd(int(b), int(m)) == 1
    except Exception:
        h3 = False

    # H_4: a == b (mod m)
    try:
        m_int = int(m)
        if m_int == 0:
            h4 = (a == b)
        else:
            h4 = (int(a) - int(b)) % m_int == 0
    except Exception:
        h4 = False

    # Conclusion: a^-1 == b^-1 (mod m)
    try:
        m_int = int(m)
        if m_int == 0:
            # Modular inverse modulo 0 is undefined in standard modular arithmetic.
            # The conclusion fails to hold.
            q = False
        else:
            inv_a = pow(int(a), -1, m_int)
            inv_b = pow(int(b), -1, m_int)
            q = (inv_a - inv_b) % m_int == 0
    except Exception:
        q = False

    neg_q = not q

    return [h1, h2, h3, h4, neg_q]