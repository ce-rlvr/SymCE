import sympy
import sympy.ntheory
from sympy import Integer

# Top-level setup
# (No specific named bindings required for this number theory problem)

def conditions(witness) -> list[bool]:
    try:
        # Check if witness is an integer-like object
        if not isinstance(witness, (int, Integer)) or isinstance(witness, bool):
            return [False]
        n = int(witness)
    except Exception:
        return [False]
        
    try:
        if n < 1:
            # For n < 1, 2^n - 1 <= 0, so multiplicative order is undefined
            neg_q = True
        elif n > 60:
            # For n >= 2, the order of 2 modulo 2^n - 1 is mathematically proven to be exactly n.
            # Proof: order k must satisfy 2^k = 1 mod (2^n - 1), so 2^k - 1 is a multiple of 2^n - 1.
            # Since k > 0, 2^k - 1 >= 2^n - 1, which implies k >= n.
            # Since 2^n = 1 mod (2^n - 1), n is a valid exponent. Thus k = n.
            # We use this shortcut for n > 60 to avoid slow factorization in n_order.
            neg_q = False
        else:
            m = 2**n - 1
            try:
                order = sympy.ntheory.n_order(2, m)
                neg_q = bool(order != n)
            except ValueError:
                # n_order raises ValueError for m <= 1 (e.g., when n = 1, m = 1)
                neg_q = True
    except Exception:
        neg_q = True
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The multiplicative order of 2 modulo 2^n - 1 is not exactly n"
]

N_HYP = 0
NEG_Q_INDEX = 0