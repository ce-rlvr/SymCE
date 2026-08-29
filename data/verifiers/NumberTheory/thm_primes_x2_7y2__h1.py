import math
import sympy

def conditions(witness):
    try:
        if isinstance(witness, bool):
            return [False]
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        p = int(witness)
    except Exception:
        return [False]

    try:
        if p < 0:
            A = False
        else:
            A = False
            max_y = math.isqrt(p // 7)
            for y in range(max_y + 1):
                rem = p - 7 * y**2
                if rem >= 0:
                    x = math.isqrt(rem)
                    if x**2 == rem:
                        A = True
                        break
    except Exception:
        A = False

    try:
        B = (p == 7) or (p % 7 in [1, 2, 4])
    except Exception:
        B = False

    neg_Q = (A != B)

    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: (∃x,y: x^2 + 7y^2 = p) is not equivalent to (p = 7 or p ≡ 1, 2, 4 mod 7)"
]

N_HYP = 0
NEG_Q_INDEX = 0