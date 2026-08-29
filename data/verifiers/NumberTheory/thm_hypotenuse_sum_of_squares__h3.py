import math
import sympy

def is_pos_int(x):
    return isinstance(x, (int, sympy.Integer)) and not isinstance(x, bool) and x > 0

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
        h1 = is_pos_int(a) and is_pos_int(b) and is_pos_int(c)
    except Exception:
        h1 = False

    try:
        a, b, c = witness
        h2 = (a**2 + b**2 == c**2)
    except Exception:
        h2 = False

    try:
        a, b, c = witness
        conclusion_holds = False
        if is_pos_int(c):
            c_int = int(c)
            limit = math.isqrt(c_int)
            for u in range(1, limit + 1):
                v2 = c_int - u**2
                if v2 > 0:
                    v = math.isqrt(v2)
                    if v**2 == v2:
                        if math.gcd(u, v) == 1:
                            conclusion_holds = True
                            break
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are positive integers",
    "H_2: a^2 + b^2 = c^2",
    "¬Q: There do not exist relatively prime positive integers u and v such that c = u^2 + v^2"
]

N_HYP = 2
NEG_Q_INDEX = 2