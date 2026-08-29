import sympy
from sympy import cos, pi, Symbol, minpoly, Rational
from sympy.ntheory import totient

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        h1 = bool(n >= 1 and n == witness)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        val = 2 * cos(2 * pi / n)
        mp = minpoly(val, x)
        deg = sympy.degree(mp, x)
        expected = Rational(totient(n), 2)
        neg_q = bool(deg != expected)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer (domain of Euler's totient function)",
    "¬Q: The degree of the minimal polynomial of 2cos(2pi/n) over Q is not phi(n)/2"
]

N_HYP = 1
NEG_Q_INDEX = 1