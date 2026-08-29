import math

def conditions(witness):
    try:
        x, y, z = witness
    except Exception:
        return [False, False, False]

    # H_1: x, y, and z are positive integers
    try:
        h1 = (isinstance(x, int) and isinstance(y, int) and isinstance(z, int) and
              not isinstance(x, bool) and not isinstance(y, bool) and not isinstance(z, bool) and
              x > 0 and y > 0 and z > 0)
    except Exception:
        h1 = False

    # H_2: x^2 + 2y^2 = z^2
    try:
        h2 = (x**2 + 2 * y**2 == z**2)
    except Exception:
        h2 = False

    # ¬Q: There do not exist coprime positive integers u and v, with u odd, 
    # such that x = |u^2 - 2v^2|, y = 2uv, and z = u^2 + 2v^2.
    try:
        q_holds = False
        if h1 and y % 2 == 0:
            k = y // 2
            for i in range(1, math.isqrt(k) + 1):
                if k % i == 0:
                    u1, v1 = i, k // i
                    u2, v2 = k // i, i
                    
                    if u1 % 2 == 1 and math.gcd(u1, v1) == 1:
                        if x == abs(u1**2 - 2 * v1**2) and z == u1**2 + 2 * v1**2:
                            q_holds = True
                            break
                            
                    if u2 % 2 == 1 and math.gcd(u2, v2) == 1:
                        if x == abs(u2**2 - 2 * v2**2) and z == u2**2 + 2 * v2**2:
                            q_holds = True
                            break
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x, y, and z are positive integers",
    "H_2: x^2 + 2y^2 = z^2",
    "¬Q: There do not exist coprime positive integers u and v, with u odd, such that x = |u^2 - 2v^2|, y = 2uv, and z = u^2 + 2v^2"
]

N_HYP = 2
NEG_Q_INDEX = 2