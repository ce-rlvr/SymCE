import sympy
import math

# Top-level setup
# No specific named bindings required for this number theory problem.

def conditions(witness) -> list[bool]:
    # H_1: n is a non-zero integer so that d(n) is well-defined and finite.
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool) and int(witness) != 0
    except Exception:
        h1 = False

    # neg_Q: The conclusion is that d(n) is odd iff n is a perfect square.
    # We negate this: d(n) is odd is NOT equivalent to n being a perfect square.
    try:
        n = int(witness)
        d_n = sympy.divisor_count(abs(n))
        is_odd = (d_n % 2 == 1)
        
        if n < 0:
            is_perfect_square = False
        else:
            is_perfect_square = (math.isqrt(n)**2 == n)
            
        neg_q = bool(is_odd != is_perfect_square)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a non-zero integer",
    "¬Q: d(n) being odd is not equivalent to n being a perfect square"
]

N_HYP = 1
NEG_Q_INDEX = 1