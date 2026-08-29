import sympy
import math

# Top-level setup
# (No specific named objects required for this number theory conjecture)

CONDITION_LABELS = [
    "H_1: phi(n) is Euler's totient function",
    "¬Q: lim_{x -> inf} (1/x^2) sum_{n <= x} phi(n) != 3/pi^2"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks whether the given witness satisfies the hypotheses and fails the conclusion.
    The witness is expected to be a function (or subscriptable object) representing phi(n).
    """
    # H_1: witness is Euler's totient function
    try:
        h1 = True
        # We check the first 1000 values to ensure it matches Euler's totient function
        for n in range(1, 1001):
            try:
                val = witness(n)
            except TypeError:
                val = witness[n]
                
            if val != sympy.totient(n):
                h1 = False
                break
    except Exception:
        h1 = False

    # neg_Q: The limit is NOT 3/pi^2
    try:
        s = 0
        # We approximate the limit by evaluating the sum up to x = 1000
        for n in range(1, 1001):
            try:
                val = witness(n)
            except TypeError:
                val = witness[n]
            s += val
        
        limit_approx = float(s) / (1000 ** 2)
        expected = 3.0 / (math.pi ** 2)
        
        # For the true Euler's totient function, the limit is exactly 3/pi^2.
        # At x = 1000, the approximation error is around 0.0002.
        # We use a threshold of 0.01 to robustly check if the limit deviates from 3/pi^2.
        neg_q = abs(limit_approx - expected) > 0.01
    except Exception:
        neg_q = False

    return [h1, neg_q]