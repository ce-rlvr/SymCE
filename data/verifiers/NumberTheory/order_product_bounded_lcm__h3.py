import sympy
import math

def get_order(x, m):
    x = int(x)
    m = int(m)
    if m == 1:
        return 1
    return sympy.ntheory.n_order(x, m)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness['n']
            a = witness['a']
            b = witness['b']
            d1 = witness['d1']
            d2 = witness['d2']
        else:
            n, a, b, d1, d2 = witness
    except Exception:
        return [False] * 4

    # H1: n is a positive integer
    try:
        h1 = (int(n) == n) and (n > 0)
    except Exception:
        h1 = False

    # H2: a and b are integers coprime to n
    try:
        h2 = (int(a) == a) and (int(b) == b) and (math.gcd(int(a), int(n)) == 1) and (math.gcd(int(b), int(n)) == 1)
    except Exception:
        h2 = False

    # H3: The multiplicative order of b modulo n is d2
    try:
        h3 = (int(d2) == d2) and (d2 > 0) and (get_order(b, n) == d2)
    except Exception:
        h3 = False

    # neg_Q: The multiplicative order of ab modulo n does NOT divide lcm(d1, d2)
    try:
        if int(d1) != d1:
            neg_q = False
        else:
            ord_ab = get_order(int(a) * int(b), int(n))
            lcm_d1_d2 = math.lcm(int(d1), int(d2))
            neg_q = (lcm_d1_d2 % ord_ab != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: a and b are integers coprime to n",
    "H_3: The multiplicative order of b modulo n is d2",
    "¬Q: The multiplicative order of ab modulo n does not divide lcm(d1, d2)"
]

N_HYP = 3
NEG_Q_INDEX = 3