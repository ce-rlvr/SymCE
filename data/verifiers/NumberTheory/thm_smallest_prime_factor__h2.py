import sympy
import math

def conditions(witness):
    # H1: Let n be an integer.
    try:
        if isinstance(witness, int) or isinstance(witness, sympy.Integer):
            if isinstance(witness, bool):
                h1 = False
            else:
                h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: n is a composite number.
    try:
        n = int(witness)
        # A composite number in the ring of integers is a non-zero non-unit 
        # that is not prime. Thus, abs(n) > 1 and abs(n) is not prime.
        if abs(n) > 1 and not sympy.isprime(abs(n)):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: There does NOT exist a prime number p such that p divides n and p <= sqrt(n).
    try:
        n = int(witness)
        if n == 0:
            neg_q = False
        else:
            factors = sympy.factorint(n)
            # Extract positive prime factors
            primes = [p for p in factors.keys() if p != -1 and sympy.isprime(p)]
            
            exists = False
            if n > 0:
                sqrt_n = math.sqrt(n)
                for p in primes:
                    if p <= sqrt_n:
                        exists = True
                        break
            else:
                # For n < 0, sqrt(n) is purely imaginary, so no real prime p can be <= sqrt(n).
                exists = False
                
            neg_q = not exists
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: n is a composite number",
    "¬Q: There is no prime p dividing n such that p <= sqrt(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2