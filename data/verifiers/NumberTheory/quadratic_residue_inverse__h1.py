import sympy
import math
import itertools
import functools

# Top-level setup
# No specific named objects are required for this number theory problem.

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        a, p = witness
        a_int = int(a)
        p_int = int(p)
        if a_int != a or p_int != p:
            return [False, False, False]
        a = a_int
        p = p_int
    except Exception:
        return [False, False, False]

    # H1: a is an integer not divisible by p
    try:
        h1 = (p != 0) and (a % p != 0)
    except Exception:
        h1 = False

    # H2: There exists an integer x such that x^2 \equiv a \pmod p
    try:
        h2 = False
        if p != 0 and abs(p) <= 1000000:
            for x in range(abs(p)):
                if (x * x) % abs(p) == a % abs(p):
                    h2 = True
                    break
    except Exception:
        h2 = False

    # neg_Q: The modular inverse a^{-1} modulo p is a quadratic residue modulo p...
    # (Negation: The modular inverse does not exist, or it is not a quadratic residue)
    try:
        neg_q = False
        if p != 0 and abs(p) <= 1000000:
            try:
                inv_a = pow(a, -1, abs(p))
                is_residue = False
                for y in range(abs(p)):
                    if (y * y) % abs(p) == inv_a % abs(p):
                        is_residue = True
                        break
                neg_q = not is_residue
            except ValueError:
                # Inverse does not exist
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer not divisible by p",
    "H_2: There exists an integer x such that x^2 \\equiv a \\pmod p",
    "¬Q: The modular inverse a^{-1} modulo p does not exist or is not a quadratic residue modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2