import math

def conditions(witness) -> list[bool]:
    try:
        p, d = witness
        p = int(p)
        d = int(d)
    except Exception:
        return [False, False]
        
    try:
        h1 = (d > 2) and ((p - 1) % d == 0)
    except Exception:
        h1 = False
        
    try:
        if p < 2:
            neg_q = True
        else:
            divisors = []
            for i in range(1, int(math.isqrt(d)) + 1):
                if d % i == 0:
                    divisors.append(i)
                    if i != d // i:
                        divisors.append(d // i)
            if d in divisors:
                divisors.remove(d)
                
            elements = []
            for x in range(1, p):
                if math.gcd(x, p) != 1:
                    continue
                if pow(x, d, p) == 1:
                    is_order_d = True
                    for k in divisors:
                        if pow(x, k, p) == 1:
                            is_order_d = False
                            break
                    if is_order_d:
                        elements.append(x)
                        
            if not elements:
                neg_q = True
            else:
                prod = 1
                for x in elements:
                    prod = (prod * x) % p
                neg_q = (prod % p != 1 % p)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: d is an integer strictly greater than 2 that divides p - 1",
    "¬Q: The product of elements of order d modulo p is not congruent to 1 (or no such elements exist)"
]

N_HYP = 1
NEG_Q_INDEX = 1