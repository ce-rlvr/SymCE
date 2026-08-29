import sympy
import sympy.ntheory

# Top-level setup
# No specific named objects required for this number theory conjecture

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False, False]
        p, x, y = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.ntheory.isprime(p))
    except Exception:
        h1 = False

    # H_2: p > 3
    try:
        h2 = bool(p > 3)
    except Exception:
        h2 = False

    # H_3: x and y are integers
    try:
        h3 = bool(sympy.S(x).is_integer and sympy.S(y).is_integer)
    except Exception:
        h3 = False

    # H_4: p divides x^2 + xy + y^2
    try:
        val = x**2 + x*y + y**2
        h4 = bool(val % p == 0)
    except Exception:
        h4 = False

    # ¬Q: p is not congruent to 1 mod 3
    try:
        neg_q = bool(p % 3 != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: p > 3",
    "H_3: x and y are integers",
    "H_4: p divides x^2 + xy + y^2",
    "¬Q: p is not congruent to 1 mod 3"
]

N_HYP = 4
NEG_Q_INDEX = 4