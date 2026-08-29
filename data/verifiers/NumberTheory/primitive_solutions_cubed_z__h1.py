import math

def conditions(witness) -> list[bool]:
    try:
        w = tuple(witness)
        if len(w) != 3:
            return [False, False]
        x, y, z = int(w[0]), int(w[1]), int(w[2])
    except Exception:
        return [False, False]
    
    try:
        h1 = (math.gcd(x, y) == 1)
    except Exception:
        h1 = False
        
    try:
        q_holds = False
        if z >= 0:
            limit = math.isqrt(z)
            for m in range(-limit, limit + 1):
                n2 = z - m**2
                if n2 < 0:
                    continue
                n_abs = math.isqrt(n2)
                if n_abs**2 == n2:
                    for n in set([n_abs, -n_abs]):
                        if math.gcd(m, n) == 1 and (m % 2) != (n % 2):
                            val1 = m**3 - 3 * m * n**2
                            val2 = 3 * m**2 * n - n**3
                            if (x == val1 and y == val2) or (x == val2 and y == val1):
                                q_holds = True
                                break
                if q_holds:
                    break
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: gcd(x, y) == 1",
    "¬Q: There do not exist m, n satisfying the conditions"
]

N_HYP = 1
NEG_Q_INDEX = 1