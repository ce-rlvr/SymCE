import sympy
from sympy.ntheory import factorint, isprime

# Top-level setup
# We evaluate the conjecture in the ring of integers ZZ.
# A witness can be an integer n (assuming P = 2*ZZ) or a tuple (ideal_gen, n).

def radical(m):
    if m == 0:
        return 0
    m = abs(m)
    if m == 1:
        return 1
    factors = factorint(m)
    res = 1
    for p in factors:
        res *= p
    return res

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) != 2:
                return [False, False, False]
            ideal_gen, n = witness
        else:
            # If only n is provided, default to the prime ideal (2) in ZZ
            ideal_gen = 2
            n = witness
            
        # H1: R is a commutative ring with identity. 
        # ZZ is a commutative ring with identity. We just require n to be a 
        # non-negative integer so that P^n is a valid ideal.
        h1 = isinstance(ideal_gen, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and n >= 0
        ideal_gen = int(ideal_gen)
        n = int(n)
    except Exception:
        h1 = False
        ideal_gen = 2
        n = 1

    try:
        # H2: P is a prime ideal of R.
        # In ZZ, an ideal (m) is prime iff m is prime or m == 0.
        h2 = isprime(abs(ideal_gen)) or ideal_gen == 0
    except Exception:
        h2 = False

    try:
        # Conclusion: The radical of P^n is equal to P.
        # Negation: The radical of P^n is NOT equal to P.
        # Optimization: radical(P^n) = radical(P) for n > 0, and R for n = 0.
        if n == 0:
            rad_pn = 1
        else:
            rad_pn = radical(ideal_gen)
            
        neg_q = abs(rad_pn) != abs(ideal_gen)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: P is a prime ideal of R",
    "¬Q: The radical of the ideal P^n is not equal to P"
]

N_HYP = 2
NEG_Q_INDEX = 2