import sympy
from sympy.ntheory import isprime, factorint
import math

def is_prime_power(n):
    if n <= 1:
        return False
    factors = factorint(n)
    return len(factors) == 1

def conditions(witness) -> list[bool]:
    """
    Given a witness (q, m, n), checks if it is a counterexample to the false conjecture.
    The conjecture claims that for any positive integers m, n and any q,
    if F_{q^m} and F_{q^n} are subfields of a common algebraic closure of F_q,
    then their intersection is F_{q^{gcd(m,n)}}.
    
    This is false if q is not a prime power, but q^m and q^n are prime powers
    (e.g., q could be a real number like sqrt(2) or a rational, but in the context of integers,
    if q is not a prime power, F_q is not a field, so the hypothesis fails.
    Wait, if q is an integer, q^m is a prime power iff q is a prime power.
    However, the witness could be a tuple of sets or fields directly, or just (q, m, n).
    We will evaluate the hypotheses strictly.)
    """
    try:
        q, m, n = witness
    except Exception:
        return [False, False, False]

    # H_1: m and n are positive integers
    try:
        h1 = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0
    except Exception:
        h1 = False

    # H_2: F_{q^m} and F_{q^n} are subfields of a common algebraic closure of F_q
    # This implies q^m and q^n are prime powers, and q is a prime power.
    try:
        h2 = is_prime_power(q) and is_prime_power(q**m) and is_prime_power(q**n)
    except Exception:
        h2 = False

    # ¬Q: The intersection F_{q^m} \cap F_{q^n} is NOT exactly the field F_{q^{\gcd(m,n)}}.
    # For finite fields, F_{p^A} \cap F_{p^B} = F_{p^{\gcd(A,B)}}.
    # So F_{q^m} \cap F_{q^n} = F_{p^{\gcd(k*m, k*n)}} = F_{p^{k*\gcd(m,n)}} = F_{q^{\gcd(m,n)}}.
    # This is a mathematical theorem, so it is ALWAYS true for valid prime powers.
    # If the verifier is called with a witness, we just check if the intersection size matches.
    try:
        if not h2:
            neg_q = False
        else:
            # The intersection of F_{q^m} and F_{q^n} has size q^{\gcd(m,n)}
            # We check if it is NOT equal to q^{\gcd(m,n)}
            # Since it is a theorem that they are equal, neg_q will evaluate to False for valid q.
            # But we must return the boolean evaluation of the negated conclusion.
            expected_size = q ** math.gcd(m, n)
            actual_size = q ** math.gcd(m, n) # By theorem
            neg_q = (actual_size != expected_size)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: F_{q^m} and F_{q^n} are subfields of a common algebraic closure of F_q",
    "¬Q: The intersection F_{q^m} \cap F_{q^n} is not exactly the field F_{q^{\gcd(m,n)}}"
]

N_HYP = 2
NEG_Q_INDEX = 2