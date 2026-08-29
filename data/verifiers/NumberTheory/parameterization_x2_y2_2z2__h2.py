import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        x, y, z = witness
    except Exception:
        return [False, False, False]

    def is_pos_int(val):
        try:
            if isinstance(val, bool):
                return False
            return int(val) == val and val > 0
        except Exception:
            return False

    # H_1: x, y, and z are positive integers
    try:
        h1 = is_pos_int(x) and is_pos_int(y) and is_pos_int(z)
    except Exception:
        h1 = False

    # H_2: x^2 + y^2 = 2z^2
    try:
        h2 = bool(x**2 + y**2 == 2 * z**2)
    except Exception:
        h2 = False

    # ¬Q: There do not exist coprime positive integers u and v of opposite parity 
    # such that x = |u^2 - 2uv - v^2|, y = |u^2 + 2uv - v^2|, and z = u^2 + v^2.
    try:
        q_holds = False
        if is_pos_int(z):
            z_int = int(z)
            x_int = int(x)
            y_int = int(y)
            limit = math.isqrt(z_int)
            for u in range(1, limit + 1):
                v2 = z_int - u**2
                if v2 <= 0:
                    continue
                v = math.isqrt(v2)
                if v**2 == v2 and v > 0:
                    if math.gcd(u, v) == 1 and (u % 2) != (v % 2):
                        if x_int == abs(u**2 - 2*u*v - v**2) and y_int == abs(u**2 + 2*u*v - v**2):
                            q_holds = True
                            break
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x, y, and z are positive integers",
    "H_2: x^2 + y^2 = 2z^2",
    "¬Q: There do not exist coprime positive integers u and v of opposite parity such that x = |u^2 - 2uv - v^2|, y = |u^2 + 2uv - v^2|, and z = u^2 + v^2"
]

N_HYP = 2
NEG_Q_INDEX = 2