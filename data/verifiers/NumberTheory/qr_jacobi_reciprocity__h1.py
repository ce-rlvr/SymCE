import sympy
from sympy import Rational
from sympy.ntheory import jacobi_symbol
import math

# Top-level setup
# (No specific named bindings needed for this number theory problem)

def conditions(witness) -> list[bool]:
    try:
        m, n = witness
    except Exception:
        return [False, False, False]

    # H1: n is an odd positive integer
    try:
        n_int = int(n)
        h1 = bool((n_int % 2 == 1) and (n_int > 0) and (n == n_int))
    except Exception:
        h1 = False

    # H2: m and n are coprime
    try:
        m_int = int(m)
        n_int = int(n)
        h2 = bool((math.gcd(m_int, n_int) == 1) and (m == m_int) and (n == n_int))
    except Exception:
        h2 = False

    # neg_Q: The Jacobi symbol product (m/n)(n/m) is equal to (-1)^((m-1)/2 * (n-1)/2).
    try:
        m_int = int(m)
        n_int = int(n)
        lhs = jacobi_symbol(m_int, n_int) * jacobi_symbol(n_int, m_int)
        rhs = (-1)**(Rational(m_int - 1, 2) * Rational(n_int - 1, 2))
        neg_q = bool(lhs != rhs)
    except Exception:
        # If jacobi_symbol raises an exception (e.g. m is even or negative),
        # the conclusion is undefined, hence it is not true that they are equal.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an odd positive integer",
    "H_2: m and n are coprime",
    "¬Q: The Jacobi symbol product (m/n)(n/m) is not equal to (-1)^((m-1)/2 * (n-1)/2) or is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2