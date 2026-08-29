import sympy

# Top-level setup
# (No named bindings needed for number theory; use integers directly)

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    """
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False, False]
    
    def is_pos_int(x):
        return (type(x) is int or isinstance(x, sympy.Integer)) and x > 0

    # H_1: a, b, and c are strictly positive integers
    try:
        h1_ok = bool(is_pos_int(a) and is_pos_int(b) and is_pos_int(c))
    except Exception:
        h1_ok = False

    # H_2: a^2 + b^2 = c^2
    try:
        h2_ok = bool(a**2 + b**2 == c**2)
    except Exception:
        h2_ok = False

    # H_3: a is an odd integer
    try:
        h3_ok = bool(a % 2 == 1)
    except Exception:
        h3_ok = False

    # ¬Q: The integer c^2 - a^2 is NOT divisible by 16
    try:
        neg_q_ok = bool((c**2 - a**2) % 16 != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "H_2: a^2 + b^2 = c^2",
    "H_3: a is an odd integer",
    "¬Q: c^2 - a^2 is not divisible by 16"
]

N_HYP = 3
NEG_Q_INDEX = 3