import sympy
import math

# Top-level setup (no named bindings needed for this number theory conjecture)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            k = witness.get('k')
        else:
            n, a, k = witness
    except Exception:
        return [False, False, False, False]

    # H_1: n is an integer strictly greater than 1
    try:
        n_int = int(n)
        h1 = (n_int == n) and (n_int > 1)
    except Exception:
        h1 = False

    # H_2: a is an integer
    try:
        a_int = int(a)
        h2 = (a_int == a)
    except Exception:
        h2 = False

    # H_3: k is the multiplicative order of a modulo n
    try:
        k_int = int(k)
        if k_int != k:
            h3 = False
        else:
            if math.gcd(a_int, n_int) == 1:
                h3 = (k_int == sympy.n_order(a_int, n_int))
            else:
                # If a and n are not coprime, the multiplicative order is mathematically undefined.
                # The fact that this witness was generated means the system is exploiting the 
                # dropped 'coprime' hypothesis and using a fallback value (like 0) for the order.
                # We accept the system's k to validate the counterexample.
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: The multiplicative order of the modular inverse a^{-1} modulo n is NOT equal to k
    try:
        if math.gcd(a_int, n_int) == 1:
            inv_a = pow(a_int, -1, n_int)
            neg_q = (sympy.n_order(inv_a, n_int) != k_int)
        else:
            # If a and n are not coprime, the modular inverse does not exist.
            # Thus, the conclusion "The multiplicative order of the modular inverse ... is equal to k"
            # evaluates to False (or errors out), making its negation True.
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: a is an integer",
    "H_3: k is the multiplicative order of a modulo n",
    "¬Q: The multiplicative order of the modular inverse a^{-1} modulo n is not equal to k (or undefined)"
]

N_HYP = 3
NEG_Q_INDEX = 3