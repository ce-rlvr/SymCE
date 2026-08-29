import sympy
import math

# Top-level setup
# (No specific named bindings required for this number theory conjecture)

def conditions(witness):
    try:
        p = int(witness)
        if p != witness:
            return [False]
    except Exception:
        return [False]
    
    try:
        # The conclusion states there exists g such that the order of g mod p is p - 1.
        # The order of any element mod p divides phi(p).
        # If p is composite, phi(p) < p - 1, so no element can have order p - 1.
        # If p is prime, phi(p) = p - 1, and primitive roots exist, so there is an element of order p - 1.
        # Thus, the conclusion fails (neg_Q is True) if and only if p is not prime.
        if p <= 1:
            neg_q = True
        else:
            neg_q = not sympy.isprime(p)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: There does not exist an integer g such that the multiplicative order of g modulo p is exactly p-1"
]

N_HYP = 0
NEG_Q_INDEX = 0