import sympy
import math

def conditions(witness):
    try:
        a, k = witness
        h1 = bool(isinstance(a, (int, sympy.Integer)) and isinstance(k, (int, sympy.Integer)) and a > 0 and k > 0)
    except Exception:
        h1 = False

    try:
        a, k = witness
        M = a**2 + k
        try:
            inv_a = sympy.mod_inverse(a, M)
            inv_k = sympy.mod_inverse(k, M)
            rhs = (-a * inv_k) % M
            neg_q = bool(inv_a != rhs)
        except ValueError:
            # If either modular inverse does not exist, the conclusion fails.
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and k are positive integers",
    "¬Q: The modular inverse of a modulo a^2+k is not congruent to -a * (k^{-1} mod (a^2+k)) mod (a^2+k) (or inverses do not exist)"
]

N_HYP = 1
NEG_Q_INDEX = 1