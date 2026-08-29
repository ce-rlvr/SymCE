import math
import sympy
from sympy.ntheory import divisor_sigma

def count_4_squares(n):
    if n < 0:
        return 0
    squares = {}
    limit = math.isqrt(n)
    for a in range(-limit, limit + 1):
        for b in range(-limit, limit + 1):
            s = a*a + b*b
            if s <= n:
                squares[s] = squares.get(s, 0) + 1
    
    count = 0
    for s, c in squares.items():
        if n - s in squares:
            count += c * squares[n - s]
    return count

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and witness > 0
    except Exception:
        h1 = False

    try:
        if h1:
            n = int(witness)
            reps = count_4_squares(n)
            expected = int(8 * divisor_sigma(n))
            neg_q = bool(reps != expected)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The number of representations of n as a sum of four squares is not exactly 8\\sigma(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1