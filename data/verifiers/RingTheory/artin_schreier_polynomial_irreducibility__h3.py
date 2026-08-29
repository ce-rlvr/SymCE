import sympy
from sympy import isprime, Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (p, a) or (F, p, a) where:
      - p is a prime number (the characteristic of the field F)
      - a is an integer representing an element of the prime field GF(p)
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                p, a = witness
            elif len(witness) == 3:
                _, p, a = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: F is a field of prime characteristic p > 0
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: a is an element of F
    try:
        # Any integer can represent an element in GF(p)
        a_val = int(a)
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: The polynomial x^p - x - a is reducible over F
    try:
        if not h1 or not h2:
            neg_q = False
        elif p > 1000:
            # Prevent timeout for excessively large primes
            neg_q = False
        else:
            poly = Poly(x**p - x - a_val, x, domain=sympy.GF(p))
            neg_q = not poly.is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of prime characteristic p > 0",
    "H_2: a is an element of F",
    "¬Q: The polynomial x^p - x - a is reducible over F"
]

N_HYP = 2
NEG_Q_INDEX = 2