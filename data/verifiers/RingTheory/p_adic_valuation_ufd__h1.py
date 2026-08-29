import math
import sympy
from sympy.abc import x, y, z
from sympy import Rational, Integer

def v(p, val, n):
    if val % n == 0:
        return float('inf')
    k = 0
    pk = 1
    while True:
        if val % math.gcd(pk, n) == 0:
            k += 1
            pk = (pk * p) % n
            if k > n + 2:
                return float('inf')
        else:
            return k - 1

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        n, p, a, b = witness
        n = int(n)
        p = int(p)
        a = int(a)
        b = int(b)
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime element of R
    try:
        if n > 1 and p % n != 0:
            g = math.gcd(p, n)
            h1 = bool((g > 1) and sympy.isprime(g))
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: v_p(x) denotes the exponent of p in the prime factorization of an element x in R \setminus {0}
    try:
        h2 = True
        for val in range(1, n):
            if v(p, val, n) == float('inf'):
                h2 = False
                break
    except Exception:
        h2 = False

    # H_3: a and b are non-zero elements of R
    try:
        h3 = bool((a % n != 0) and (b % n != 0))
    except Exception:
        h3 = False

    # ¬Q: v_p(ab) != v_p(a) + v_p(b)
    try:
        v_ab = v(p, (a * b) % n, n)
        v_a = v(p, a % n, n)
        v_b = v(p, b % n, n)
        neg_q = bool(v_ab != v_a + v_b)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime element of R",
    "H_2: v_p(x) denotes the exponent of p in the prime factorization of an element x in R \\setminus {0}",
    "H_3: a and b are non-zero elements of R",
    "¬Q: v_p(ab) != v_p(a) + v_p(b)"
]

N_HYP = 3
NEG_Q_INDEX = 3