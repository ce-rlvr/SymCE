import sympy

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture.
    The conjecture claims that n and n+1 are coprime integers.
    Since there are no remaining hypotheses, we only check if the conclusion fails.
    """
    try:
        # The conclusion states that n is an integer and gcd(n, n+1) == 1.
        if isinstance(witness, (int, sympy.Integer)):
            q = (sympy.gcd(witness, witness + 1) == 1)
        else:
            # If n is not an integer, the statement "The integers n and n+1..." is false.
            q = False
        
        neg_q = not q
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: n and n+1 are not coprime integers"
]

N_HYP = 0
NEG_Q_INDEX = 0