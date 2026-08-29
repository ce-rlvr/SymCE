import sympy
import math

Z = "Z"

def conditions(witness):
    try:
        if isinstance(witness, dict):
            ring = witness.get('R', Z)
            q1 = witness.get('Q_1', witness.get('Q1'))
            p1 = witness.get('P_1', witness.get('P1'))
            q2 = witness.get('Q_2', witness.get('Q2'))
            p2 = witness.get('P_2', witness.get('P2'))
        elif len(witness) == 5:
            ring, q1, p1, q2, p2 = witness
        elif len(witness) == 4:
            ring = Z
            q1, p1, q2, p2 = witness
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    def is_ideal(a):
        if isinstance(a, int):
            return True
        if hasattr(a, 'is_Integer') and a.is_Integer:
            return True
        return False

    def to_int(a):
        return int(a)

    def contains(a, b):
        a = abs(to_int(a))
        b = abs(to_int(b))
        if a == 0:
            return b == 0
        return b % a == 0

    def intersection(a, b):
        a = abs(to_int(a))
        b = abs(to_int(b))
        if a == 0 or b == 0:
            return 0
        return (a * b) // math.gcd(a, b)

    def radical(a):
        a = abs(to_int(a))
        if a == 0:
            return 0
        if a == 1:
            return 1
        factors = sympy.ntheory.factorint(a)
        res = 1
        for p in factors:
            res *= p
        return res

    def is_primary(a):
        a = abs(to_int(a))
        if a == 0:
            return True
        if a == 1:
            return False
        factors = sympy.ntheory.factorint(a)
        return len(factors) == 1

    try:
        h1 = (ring == Z) and all(is_ideal(x) for x in [q1, p1, q2, p2])
    except Exception:
        h1 = False

    try:
        h2 = is_primary(q1) and radical(q1) == abs(to_int(p1))
    except Exception:
        h2 = False

    try:
        h3 = is_primary(q2) and radical(q2) == abs(to_int(p2))
    except Exception:
        h3 = False

    try:
        h4 = not contains(p1, p2)
    except Exception:
        h4 = False

    try:
        q_int = intersection(q1, q2)
        neg_q = is_primary(q_int)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Q_1 is a P_1-primary ideal in R",
    "H_3: Q_2 is a P_2-primary ideal in R",
    "H_4: P_2 is not contained in P_1",
    "¬Q: Q_1 \\cap Q_2 is a primary ideal"
]

N_HYP = 4
NEG_Q_INDEX = 4