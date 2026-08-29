import sympy
import math

# Top-level setup
# No specific named bindings needed for this number theory / field theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness['p']
            n = witness['n']
        else:
            p, n = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(sympy.isprime(p))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(isinstance(n, (int, sympy.Integer)) and n >= 1)
    except Exception:
        h2_ok = False

    try:
        p_int = int(p)
        n_int = int(n)
        # The conclusion states that the extension Q_p(zeta_n) is unramified over Q_p
        # and its degree is equal to the multiplicative order of p modulo n.
        # If gcd(p, n) > 1, the multiplicative order of p modulo n is undefined,
        # and the extension is typically ramified. Thus, the conclusion fails.
        # If gcd(p, n) == 1, the extension is unramified and its degree is the order,
        # so the conclusion holds.
        # We want neg_Q to be True when the conclusion FAILS.
        neg_q_ok = bool(math.gcd(p_int, n_int) > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: n is a positive integer",
    "¬Q: The extension is ramified or its degree does not equal the multiplicative order of p modulo n"
]

N_HYP = 2
NEG_Q_INDEX = 2