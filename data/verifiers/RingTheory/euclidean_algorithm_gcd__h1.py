import sympy
from sympy import abc

x = abc.x
y = abc.y
z = abc.z

def conditions(witness) -> list[bool]:
    try:
        a, b, r = witness
    except Exception:
        return [False, False, False]

    # H_1: a and b are non-zero elements of R
    try:
        h1 = (a != 0) and (b != 0)
    except Exception:
        h1 = False

    # H_2: r is the last non-zero remainder produced by the Euclidean algorithm applied to a and b
    try:
        u, v = a, b
        while v != 0:
            _, rem = sympy.div(u, v)
            u, v = v, rem
        h2 = (r == u)
    except Exception:
        h2 = False

    # ¬Q: r is not a greatest common divisor of a and b
    try:
        actual_gcd = sympy.gcd(a, b)
        # r is a GCD iff it associates with the actual GCD
        divides_actual = (sympy.rem(actual_gcd, r) == 0)
        actual_divides_r = (sympy.rem(r, actual_gcd) == 0)
        is_gcd = divides_actual and actual_divides_r
        neg_q = not is_gcd
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS: list[str] = [
    "H_1: a and b are non-zero",
    "H_2: r is the last non-zero remainder of Euclidean algorithm",
    "¬Q: r is not a greatest common divisor of a and b"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2