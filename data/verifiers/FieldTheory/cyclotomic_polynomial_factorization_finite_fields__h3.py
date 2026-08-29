import math
from sympy.ntheory import factorint

# Top-level setup
# No named bindings needed for this domain (Number theory / Field theory uses integers directly)

def conditions(witness):
    """
    Checks the remaining hypotheses and the negated conclusion for the false conjecture.
    The witness is expected to be a tuple (q, n, d) or a dict with these keys,
    since the variable 'd' is unbound in the conjecture's hypotheses.
    """
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
            d = witness.get('d')
        else:
            q, n, d = witness
    except Exception:
        return [False, False, False]

    # H_1: Let F_q be a finite field (i.e., q is a prime power)
    try:
        h1 = False
        if isinstance(q, int) and q >= 2:
            factors = factorint(q)
            if len(factors) == 1:
                h1 = True
    except Exception:
        h1 = False

    # H_2: Let n be a positive integer such that gcd(q, n) = 1
    try:
        h2 = False
        if isinstance(n, int) and n >= 1:
            if math.gcd(q, n) == 1:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: The conclusion FAILS.
    # Conclusion: Phi_n(x) factors over F_q into distinct monic irreducible polynomials of degree exactly d.
    # Under H1 and H2, Phi_n(x) always factors into distinct monic irreducible polynomials of degree ord_n(q).
    # Thus, the conclusion holds if and only if d == ord_n(q).
    # The negated conclusion is True if d != ord_n(q).
    try:
        neg_q = False
        if not (isinstance(d, int) and d >= 1):
            # If d is not a positive integer, it cannot be the degree of the factors.
            neg_q = True
        else:
            if n == 1:
                actual_d = 1
            else:
                actual_d = 1
                val = q % n
                while val != 1:
                    val = (val * q) % n
                    actual_d += 1
                    # Safety break in case of invalid witness where gcd(q, n) != 1
                    if actual_d > n + 1:
                        break
            if d != actual_d:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field (q is a prime power)",
    "H_2: n is a positive integer such that gcd(q, n) == 1",
    "¬Q: The irreducible factors of Phi_n(x) over F_q do not all have degree exactly d"
]

N_HYP = 2
NEG_Q_INDEX = 2