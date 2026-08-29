import math
import sympy
from sympy import Rational, Integer

# Top-level setup: named object bindings that the witness expression may reference.
# We represent the ring Z_n as the integer n (with Z_0 representing Z).
Z = 0
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to represent (R, S, x) or (R, S, f, x) where R and S are rings Z_n and Z_m.
    We extract n, m, and x as integers.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('R', witness.get('n'))
            m = witness.get('S', witness.get('m'))
            x = witness.get('x')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                n, m, x = witness
            elif len(witness) == 4:
                n, m, f, x = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        n = int(n)
        m = int(m)
        x = int(x)
    except Exception:
        return [False, False, False, False]

    # H_1: R and S are rings
    # Represented by n >= 0 and m >= 0 (where 0 represents the ring of integers Z)
    try:
        h1_ok = (n >= 0) and (m >= 0)
    except Exception:
        h1_ok = False

    # H_2: f: R -> S is a surjective ring homomorphism
    # The natural projection Z_n -> Z_m is a surjective ring homomorphism iff m divides n.
    try:
        if m == 0:
            h2_ok = (n == 0)
        else:
            h2_ok = (n % m == 0)
    except Exception:
        h2_ok = False

    # H_3: f(x) is a unit in S
    # In Z_m, an element x is a unit iff gcd(x, m) == 1.
    try:
        h3_ok = (math.gcd(x, m) == 1)
    except Exception:
        h3_ok = False

    # ¬Q: x is not a unit in R
    # In Z_n, an element x is a unit iff gcd(x, n) == 1. We want this to be FALSE.
    try:
        neg_q_ok = (math.gcd(x, n) != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a surjective ring homomorphism",
    "H_3: f(x) is a unit in S",
    "¬Q: x is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3