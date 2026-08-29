import math
import sympy
from sympy import symbols

# Top-level setup for ring theory witnesses
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    Given a witness representing ideals in the ring of integers Z,
    checks if it is a valid counterexample.
    The witness should be a tuple (a, b, p) where:
      - I = (a)
      - J = (b)
      - P = (p)
    """
    try:
        if isinstance(witness, dict):
            a = int(witness.get('a', witness.get('I')))
            b = int(witness.get('b', witness.get('J')))
            p = int(witness.get('p', witness.get('P')))
        else:
            a, b, p = witness
            a = int(a)
            b = int(b)
            p = int(p)
    except Exception:
        return [False, False, False, False]

    try:
        # H_1: R is a commutative ring.
        # We evaluate the witness in Z, which is inherently a commutative ring.
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # H_2: I and J are comaximal ideals of R.
        # In Z, ideals (a) and (b) are comaximal iff gcd(a, b) == 1.
        h2_ok = (math.gcd(a, b) == 1)
    except Exception:
        h2_ok = False

    try:
        # H_3: P is a prime ideal of R.
        # In Z, (p) is a prime ideal iff p is a prime number.
        h3_ok = sympy.isprime(p)
    except Exception:
        h3_ok = False

    try:
        # Conclusion: Either I \subseteq P or J \subseteq P, but not both.
        # I \subseteq P iff p divides a.
        # J \subseteq P iff p divides b.
        i_sub_p = (a % p == 0)
        j_sub_p = (b % p == 0)
        
        # Negated conclusion: It is NOT the case that exactly one is contained in P.
        neg_q_ok = not (i_sub_p ^ j_sub_p)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are comaximal ideals of R",
    "H_3: P is a prime ideal of R",
    "¬Q: It is not the case that exactly one of I or J is contained in P"
]

N_HYP = 3
NEG_Q_INDEX = 3