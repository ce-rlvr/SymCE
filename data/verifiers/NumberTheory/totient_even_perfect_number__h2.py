import sympy
from sympy import isprime, totient

# Top-level setup
# No specific named bindings are required for this number theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Given a witness (expected to be a tuple (p, n) or a dict with keys 'p' and 'n'),
    evaluates the remaining hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            p = witness['p']
            n = witness['n']
        else:
            p, n = witness
        p = int(p)
        n = int(n)
    except Exception:
        return [False, False]

    # H_1: p is a prime number such that 2^p - 1 is prime
    try:
        h1 = bool(isprime(p) and isprime(2**p - 1))
    except Exception:
        h1 = False

    # ¬Q: \phi(n) != 2^{p-1}(2^{p-1} - 1)
    try:
        phi_n = totient(n)
        expected = (2**(p - 1)) * (2**(p - 1) - 1)
        neg_q = bool(phi_n != expected)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number such that 2^p - 1 is prime",
    "¬Q: phi(n) != 2^{p-1}(2^{p-1} - 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1