import math
from sympy.ntheory import n_order

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 5:
            n, a, b, d, k = witness
            k_provided = True
        elif len(witness) == 4:
            n, a, b, d = witness
            k_provided = False
        else:
            return [False] * 5
        
        n = int(n)
        a = int(a)
        b = int(b)
        d = int(d)
        if k_provided:
            k = int(k)
    except Exception:
        return [False] * 5

    # H_1: n is an integer greater than 1
    try:
        h1 = (n > 1)
    except Exception:
        h1 = False

    # H_2: a and b are integers coprime to n
    try:
        h2 = (math.gcd(a, n) == 1 and math.gcd(b, n) == 1)
    except Exception:
        h2 = False

    # H_3: d is the multiplicative order of a modulo n
    try:
        if math.gcd(a, n) == 1 and n > 1:
            h3 = (n_order(a, n) == d)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: b ≡ a^k (mod n)
    try:
        if k_provided:
            h4 = ((b - pow(a, k, n)) % n == 0)
        else:
            h4 = False
            curr = 1
            b_mod = b % n
            for _ in range(min(n, 100000)):
                if curr == b_mod:
                    h4 = True
                    break
                curr = (curr * a) % n
    except Exception:
        h4 = False

    # ¬Q: The multiplicative order of b modulo n is NOT equal to d
    try:
        if math.gcd(b, n) == 1 and n > 1:
            neg_q = (n_order(b, n) != d)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: a and b are integers coprime to n",
    "H_3: d is the multiplicative order of a modulo n",
    "H_4: b is congruent to a^k modulo n",
    "¬Q: The multiplicative order of b modulo n is not equal to d"
]

N_HYP = 4
NEG_Q_INDEX = 4