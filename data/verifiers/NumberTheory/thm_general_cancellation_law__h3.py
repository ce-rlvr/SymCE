import math

# Top-level setup
# (No named bindings needed for this number theory conjecture; integers are used directly)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should provide values for a, b, c, m, and d.
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            c = witness['c']
            m = witness['m']
            d = witness['d']
        else:
            a, b, c, m, d = witness
    except Exception:
        return [False, False, False]

    # H_1: Let a, b, c, m, and d be integers with m > 0
    try:
        h1_ok = (isinstance(a, int) and isinstance(b, int) and 
                 isinstance(c, int) and isinstance(m, int) and 
                 isinstance(d, int) and m > 0)
    except Exception:
        h1_ok = False

    # H_2: Assume ac ≡ bc (mod m)
    try:
        h2_ok = ((a * c) % m == (b * c) % m)
    except Exception:
        h2_ok = False

    # ¬Q: The conclusion a ≡ b (mod m/d) FAILS.
    # This means either m/d is undefined/not an integer, or a ≢ b (mod m/d).
    try:
        if d == 0:
            neg_q_ok = True
        elif m % d != 0:
            neg_q_ok = True
        else:
            neg_q_ok = ((a - b) % (m // d) != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a, b, c, m, d are integers with m > 0",
    "H_2: ac ≡ bc (mod m)",
    "¬Q: a ≢ b (mod m/d) or m/d is not a valid integer modulus"
]

N_HYP = 2
NEG_Q_INDEX = 2