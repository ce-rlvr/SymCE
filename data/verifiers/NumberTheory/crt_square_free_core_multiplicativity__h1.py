import sympy
import sympy.ntheory
import math

def core(n):
    if n <= 0:
        raise ValueError("core is only defined for positive integers")
    f = sympy.ntheory.factorint(n)
    c = 1
    for p, e in f.items():
        if e % 2 == 1:
            c *= p
    return c

def conditions(witness):
    try:
        # Witness should be a pair of integers (a, b)
        if len(witness) != 2:
            return [False, False, False]
        a, b = witness
    except Exception:
        return [False, False, False]

    # H_1: a and b are positive integers
    try:
        a_int = int(a)
        b_int = int(b)
        h1 = (a_int == a) and (b_int == b) and (a_int > 0) and (b_int > 0)
    except Exception:
        h1 = False

    # H_2: gcd(a, b) = 1
    try:
        h2 = math.gcd(int(a), int(b)) == 1
    except Exception:
        h2 = False

    # ¬Q: core(ab) != core(a)core(b)
    try:
        neg_q = core(int(a) * int(b)) != core(int(a)) * core(int(b))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are positive integers",
    "H_2: gcd(a, b) = 1",
    "¬Q: core(ab) != core(a)core(b)"
]

N_HYP = 2
NEG_Q_INDEX = 2