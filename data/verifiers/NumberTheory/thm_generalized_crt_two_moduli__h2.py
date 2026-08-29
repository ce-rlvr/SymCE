import math

# Top-level setup
# (No named bindings needed for this Number Theory conjecture; use integers directly)

def conditions(witness) -> list[bool]:
    m, n, d, a, b = None, None, None, None, None
    try:
        if isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
            d = witness.get('d')
            a = witness.get('a')
            b = witness.get('b')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 5:
                m, n, d, a, b = witness
            elif len(witness) == 4:
                m, n, a, b = witness
            elif len(witness) == 3:
                m, n, d = witness
            elif len(witness) == 2:
                m, n = witness
    except Exception:
        pass

    # H_1: m and n are positive integers
    try:
        h1 = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0
    except Exception:
        h1 = False

    # H_2: d = gcd(m, n)
    try:
        if d is None:
            if h1:
                d_val = math.gcd(m, n)
                h2 = True
            else:
                d_val = None
                h2 = False
        else:
            d_val = d
            if h1:
                h2 = (d_val == math.gcd(m, n))
            else:
                h2 = False
    except Exception:
        h2 = False
        d_val = None

    # ¬Q: The conclusion fails
    # The conclusion states: "The system ... has a solution iff a ≡ b (mod d), AND the solution is unique..."
    # If a ≢ b (mod d), there is no solution. The phrasing "and the solution is unique" implies existence.
    # Thus, the conclusion evaluates to False (i.e., ¬Q is True) whenever a ≢ b (mod d).
    try:
        if not h1 or d_val is None:
            neg_q = False
        else:
            if a is not None and b is not None:
                if isinstance(a, int) and isinstance(b, int):
                    neg_q = (a % d_val != b % d_val)
                else:
                    neg_q = False
            else:
                # If a and b are not provided, the witness is a counterexample to the universally
                # quantified statement if there exist ANY a, b that make the conclusion fail.
                # This is possible if and only if d > 1.
                neg_q = (d_val > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "H_2: d = gcd(m, n)",
    "¬Q: The conclusion fails (the system does not have a unique solution for all a, b)"
]

N_HYP = 2
NEG_Q_INDEX = 2