import sympy
from sympy import minpoly, degree
from sympy.abc import x

def conditions(witness):
    # H_1: a is a complex number
    try:
        if isinstance(witness, str):
            h1_ok = False
        else:
            # If it can be evaluated to a Python complex number, it is a valid complex number
            # This correctly rejects free symbols, matrices, and complex infinity (zoo)
            _ = complex(witness)
            h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: The degree of the extension Q(a) over Q is NOT equal to 2^k for some non-negative integer k
    try:
        poly = minpoly(witness, x)
        d = int(degree(poly, x))
        if d <= 0:
            neg_q_ok = True
        else:
            is_pow2 = (d & (d - 1)) == 0
            neg_q_ok = not is_pow2
    except Exception as e:
        # If the number is transcendental (e.g., pi, E), it is not algebraic over Q.
        # Its degree is infinite, which is not a power of 2.
        if type(e).__name__ == 'NotAlgebraic':
            neg_q_ok = True
        else:
            neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a is a complex number",
    "¬Q: The degree of the extension Q(a) over Q is not equal to 2^k for any non-negative integer k"
]

N_HYP = 1
NEG_Q_INDEX = 1