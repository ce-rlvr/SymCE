import math
import sympy
from sympy.ntheory import divisors, mobius

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            q1 = witness.get('q1')
            q2 = witness.get('q2')
        else:
            n, q1, q2 = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(n, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        h2 = (isinstance(q1, (int, sympy.Integer)) and 
              isinstance(q2, (int, sympy.Integer)) and 
              int(q1) > 0 and int(q2) > 0 and 
              math.gcd(int(q1), int(q2)) == 1)
    except Exception:
        h2 = False

    try:
        def c(q, n_val):
            g = math.gcd(int(n_val), int(q))
            return sum(d * mobius(q // d) for d in divisors(g))
            
        neg_q = c(int(q1) * int(q2), int(n)) != c(int(q1), int(n)) * c(int(q2), int(n))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: q1 and q2 are positive integers such that gcd(q1, q2) == 1",
    "¬Q: c_{q1 q2}(n) != c_{q1}(n) c_{q2}(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2