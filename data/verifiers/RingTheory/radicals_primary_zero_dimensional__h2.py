import sympy
from sympy.ntheory import factorint
import math

x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        n, q = witness
        n = int(n)
        q = int(q)
    except Exception:
        return [False, False]

    try:
        h1 = (n >= 2)
    except Exception:
        h1 = False

    try:
        d = math.gcd(q, n)
        prime_factors = list(factorint(d).keys())
        is_maximal = (len(prime_factors) == 1)
        neg_q = not is_maximal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a zero-dimensional commutative ring (represented as Z/nZ)",
    "¬Q: The radical of Q is not a maximal ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1