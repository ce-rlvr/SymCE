import sympy

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness is expected to provide values for n, a, b, and c.
    It can be a dictionary, an object with attributes, or a tuple/list of length 4.
    """
    n, a, b, c = None, None, None, None
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
        elif hasattr(witness, 'n') and hasattr(witness, 'a') and hasattr(witness, 'b') and hasattr(witness, 'c'):
            n = witness.n
            a = witness.a
            b = witness.b
            c = witness.c
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 4:
                n, a, b, c = witness
    except Exception:
        pass

    # H_1: n is a positive integer
    try:
        h1 = (int(n) == n) and (n > 0)
    except Exception:
        h1 = False

    # H_2: a = F_n F_{n+3}
    try:
        h2 = bool(a == sympy.fibonacci(int(n)) * sympy.fibonacci(int(n) + 3))
    except Exception:
        h2 = False

    # H_3: b = 2 F_{n+1} F_{n+2}
    try:
        h3 = bool(b == 2 * sympy.fibonacci(int(n) + 1) * sympy.fibonacci(int(n) + 2))
    except Exception:
        h3 = False

    # ¬Q: a^2 + b^2 != c^2
    try:
        neg_q = bool(a**2 + b**2 != c**2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: a = F_n F_{n+3}",
    "H_3: b = 2 F_{n+1} F_{n+2}",
    "¬Q: a^2 + b^2 != c^2"
]

N_HYP = 3
NEG_Q_INDEX = 3