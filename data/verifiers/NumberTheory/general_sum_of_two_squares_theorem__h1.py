import math
import sympy
from sympy.ntheory import factorint

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        if n != witness:
            return [False]
    except Exception:
        return [False]
        
    try:
        if n < 0:
            p_n = False
        else:
            p_n = False
            limit = math.isqrt(n)
            for x in range(limit + 1):
                y2 = n - x*x
                if y2 < 0:
                    continue
                y = math.isqrt(y2)
                if y*y == y2:
                    p_n = True
                    break
    except Exception:
        p_n = False

    try:
        if n == 0:
            q_n = True
        else:
            factors = factorint(abs(n))
            q_n = True
            for p, e in factors.items():
                if p == 0: 
                    continue
                if p % 4 == 3 and e % 2 != 0:
                    q_n = False
                    break
    except Exception:
        q_n = False

    try:
        neg_q = (p_n != q_n)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The biconditional fails (x^2+y^2=n has integer solutions iff v_p(n) is even for all p=3 mod 4)"
]

N_HYP = 0
NEG_Q_INDEX = 0