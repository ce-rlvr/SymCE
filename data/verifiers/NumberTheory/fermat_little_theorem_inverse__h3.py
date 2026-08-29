import sympy
import math

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        a, p = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    try:
        h2 = isinstance(a, int) or (hasattr(a, 'is_integer') and a.is_integer)
    except Exception:
        h2 = False

    try:
        rhs = pow(int(a), int(p) - 2, int(p))
        try:
            lhs = sympy.mod_inverse(a, p)
            neg_q = bool(lhs != rhs)
        except ValueError:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: a is an integer",
    "¬Q: The modular inverse of a modulo p is not congruent to a^{p-2} mod p (or does not exist)"
]

N_HYP = 2
NEG_Q_INDEX = 2