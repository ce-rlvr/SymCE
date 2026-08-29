import sympy
from sympy import gcd, lcm
from sympy.ntheory import totient

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
    except Exception:
        return [False]

    try:
        lhs = totient(a) * totient(b)
        rhs = totient(gcd(a, b)) * totient(lcm(a, b))
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: phi(a)phi(b) != phi(gcd(a,b))phi(lcm(a,b))"
]

N_HYP = 0
NEG_Q_INDEX = 0