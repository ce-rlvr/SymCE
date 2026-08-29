import math

def conditions(witness):
    try:
        n, a, b = witness
        n_int = int(n)
        a_int = int(a)
        b_int = int(b)
    except Exception:
        return [False] * 5

    try:
        h1 = (n_int == n) and (n_int > 1)
    except Exception:
        h1 = False

    try:
        h2 = (a_int == a) and (b_int == b)
    except Exception:
        h2 = False

    try:
        h3 = math.gcd(a_int, n_int) == 1
    except Exception:
        h3 = False

    try:
        h4 = math.gcd(b_int, n_int) == 1
    except Exception:
        h4 = False

    try:
        inv_a = pow(a_int, -1, n_int)
        inv_b = pow(b_int, -1, n_int)
        sum_inv = (inv_a + inv_b) % n_int
        lhs = pow(sum_inv, -1, n_int)
        rhs = (a_int * pow(a_int + b_int, -1, n_int) * b_int) % n_int
        q = (lhs == rhs)
    except Exception:
        # If any inverse does not exist, the equation is undefined and thus fails
        q = False

    neg_q = not q

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: a and b are integers",
    "H_3: gcd(a, n) = 1",
    "H_4: gcd(b, n) = 1",
    "¬Q: (a^{-1} + b^{-1})^{-1} == a(a+b)^{-1}b mod n fails (or is undefined)"
]

N_HYP = 4
NEG_Q_INDEX = 4