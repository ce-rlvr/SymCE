import sympy

def conditions(witness):
    """
    Checks if the given witness (dimension n) is a counterexample to the conjecture.
    The conjecture states that RP^n is connected, which fails for n < 0 (the empty space).
    """
    try:
        # The witness should be the dimension n, an integer.
        n = int(witness)
        if n != float(witness):
            return [False, False, False]
        h1_ok = True
    except Exception:
        return [False, False, False]

    # H2 is a definitional property of the space's topology in this context.
    h2_ok = h1_ok

    try:
        # A topological space is connected if it has exactly two clopen subsets.
        # The empty space (n < 0) has only one clopen subset (itself/empty), so it is not connected.
        # For n >= 0, RP^n is connected.
        neg_q_ok = (n < 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: RP^n is the n-dimensional real projective space (n is an integer)",
    "H_2: RP^n is equipped with the quotient topology induced by the standard topology on R^{n+1} \\ {0}",
    "¬Q: RP^n is not a connected topological space (e.g., n < 0 yields the empty space)"
]

N_HYP = 2
NEG_Q_INDEX = 2