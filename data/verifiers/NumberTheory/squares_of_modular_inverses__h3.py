import sympy
import math
import itertools
import functools

# Top-level setup
# (No specific named bindings needed for this Number Theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple: (m, a, x)
        if len(witness) != 3:
            return [False, False, False, False]
        m, a, x = witness
    except Exception:
        return [False, False, False, False]

    def is_int(val):
        return (isinstance(val, int) or isinstance(val, sympy.Integer)) and not isinstance(val, bool)

    # H_1: m > 1 is an integer
    try:
        h1 = is_int(m) and m > 1
    except Exception:
        h1 = False

    # H_2: a is an integer
    try:
        h2 = is_int(a)
    except Exception:
        h2 = False

    # H_3: x is an integer such that x^2 \equiv a \pmod m
    try:
        h3 = is_int(x) and (int(x)**2) % int(m) == int(a) % int(m)
    except Exception:
        h3 = False

    # ¬Q: The square of the modular inverse of x, (x^{-1})^2, is congruent to a^{-1} \pmod m
    # We want neg_q to be True if this conclusion FAILS.
    try:
        m_int = int(m)
        a_int = int(a)
        x_int = int(x)
        
        try:
            # pow(base, -1, mod) computes the modular inverse.
            # It raises ValueError if the inverse does not exist.
            inv_x = pow(x_int, -1, m_int)
            inv_a = pow(a_int, -1, m_int)
            conclusion_holds = ((inv_x ** 2) % m_int == inv_a % m_int)
        except ValueError:
            # If either inverse does not exist, the statement about them being congruent is false.
            conclusion_holds = False
            
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m > 1 is an integer",
    "H_2: a is an integer",
    "H_3: x is an integer such that x^2 \\equiv a \\pmod m",
    "¬Q: The square of the modular inverse of x is not congruent to a^{-1} \\pmod m (or inverses do not exist)"
]

N_HYP = 3
NEG_Q_INDEX = 3