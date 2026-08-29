import sympy

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (a, b, c), checks if it is a valid counterexample to the false conjecture.
    """
    try:
        # Witness is expected to be a tuple of three elements (a, b, c)
        if len(witness) != 3:
            return [False, False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False, False]

    # H_1: R is a unique factorization domain.
    # We verify this by checking if the elements belong to the ring of integers (Z),
    # which is a well-known unique factorization domain.
    try:
        h1 = all(isinstance(x, (int, sympy.Integer)) for x in (a, b, c))
    except Exception:
        h1 = False

    # H_2: a, b, and c are non-zero elements of R.
    try:
        h2 = (a != 0) and (b != 0) and (c != 0)
    except Exception:
        h2 = False

    # H_3: a and b are coprime (their greatest common divisor is a unit).
    # In Z, the only units are 1 and -1, and sympy.gcd always returns a non-negative generator.
    try:
        h3 = (sympy.gcd(a, b) == 1)
    except Exception:
        h3 = False

    # ¬Q: a does not divide c.
    try:
        neg_q = (c % a != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, and c are non-zero elements of R",
    "H_3: a and b are coprime",
    "¬Q: a does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3