import sympy
import math

# Top-level setup
# No named bindings needed for this number theory problem.

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False]
        
    # H_1: a, b, c are positive integers such that a^2 + b^2 = c^2
    try:
        is_pos_int = all(isinstance(x, (int, sympy.Integer)) and x > 0 for x in witness)
        is_pythagorean = (a**2 + b**2 == c**2)
        h1_ok = bool(is_pos_int and is_pythagorean)
    except Exception:
        h1_ok = False
        
    # H_2: \gcd(a, b, c) = 1
    try:
        h2_ok = bool(math.gcd(math.gcd(int(a), int(b)), int(c)) == 1)
    except Exception:
        h2_ok = False
        
    # ¬Q: The set of side lengths {a, b, c} is not exactly {5, 12, 13}
    try:
        neg_q_ok = bool(set(int(x) for x in witness) != {5, 12, 13})
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a, b, c are positive integers such that a^2 + b^2 = c^2",
    "H_2: gcd(a, b, c) = 1",
    "¬Q: The set of side lengths {a, b, c} is not exactly {5, 12, 13}"
]

N_HYP = 2
NEG_Q_INDEX = 2