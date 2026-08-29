import sympy
from sympy import gcd

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of three elements (a, b, c) in a UFD (e.g., integers).
    """
    try:
        if len(witness) != 3:
            return [False] * 5
        a, b, c = witness
    except Exception:
        return [False] * 5

    # H_1: R is a Unique Factorization Domain
    # We verify this by checking if the elements are integers (Z is a UFD).
    try:
        h1 = all(isinstance(val, (int, sympy.Integer)) or 
                 (isinstance(val, sympy.Rational) and val.q == 1) 
                 for val in (a, b, c))
    except Exception:
        h1 = False

    # H_2: a, b, and c are non-zero elements in R
    try:
        h2 = (a != 0) and (b != 0) and (c != 0)
    except Exception:
        h2 = False

    # H_3: The elements a and b are coprime (gcd is a unit, which is 1 in Z)
    try:
        h3 = (gcd(a, b) == 1)
    except Exception:
        h3 = False

    # H_4: b divides c in R
    try:
        h4 = (c % b == 0)
    except Exception:
        h4 = False

    # ¬Q: The product ab does NOT divide c in R
    try:
        neg_q = (c % (a * b) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain (elements are integers)",
    "H_2: a, b, and c are non-zero elements",
    "H_3: a and b are coprime",
    "H_4: b divides c",
    "¬Q: The product ab does not divide c"
]

N_HYP = 4
NEG_Q_INDEX = 4