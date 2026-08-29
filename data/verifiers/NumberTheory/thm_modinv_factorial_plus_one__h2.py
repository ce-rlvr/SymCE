import sympy
import math

def conditions(witness) -> list[bool]:
    try:
        # H_1: a is an integer
        if isinstance(witness, bool):
            h1 = False
        elif isinstance(witness, (int, sympy.Integer)):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            a = int(witness)
            if a <= 0:
                # For a <= 0, factorial is undefined or division by zero occurs,
                # so the conclusion formula is invalid/undefined.
                neg_q = True
            elif a > 100000:
                # Prevent timeout for absurdly large witnesses
                neg_q = False
            else:
                fact_a = math.factorial(a)
                modulus = fact_a + 1
                inv_val = modulus - fact_a // a
                
                is_inverse = ((a * inv_val) % modulus == 1)
                neg_q = not is_inverse
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "¬Q: The modular inverse of a modulo a! + 1 is not a! + 1 - a!/a"
]

N_HYP = 1
NEG_Q_INDEX = 1