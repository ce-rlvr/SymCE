import sympy
from sympy.ntheory import totient

# Top-level setup (no specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        n, a = witness
    except Exception:
        return [False, False, False]

    # H_1: n is an integer strictly greater than 1
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool) and n > 1
    except Exception:
        h1 = False

    # H_2: a is an integer
    try:
        h2 = isinstance(a, (int, sympy.Integer)) and not isinstance(a, bool)
    except Exception:
        h2 = False

    # ¬Q: The modular inverse of a modulo n is not congruent to a^{\phi(n)-1} (mod n)
    # This means a^{\phi(n)-1} does NOT act as the modular inverse of a modulo n.
    # It acts as the inverse iff a * a^{\phi(n)-1} ≡ 1 (mod n).
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n_int = int(n)
            a_int = int(a)
            phi_n = int(totient(n_int))
            # Calculate x = a^{\phi(n)-1} mod n
            x = pow(a_int, phi_n - 1, n_int)
            # Check if x is the modular inverse of a modulo n
            neg_q = (a_int * x) % n_int != 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: a is an integer",
    "¬Q: The modular inverse of a modulo n is not congruent to a^{\\phi(n)-1} (mod n)"
]

N_HYP = 2
NEG_Q_INDEX = 2