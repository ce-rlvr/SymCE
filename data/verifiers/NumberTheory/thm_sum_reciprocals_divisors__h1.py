import sympy

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    # H_1: n is a non-zero integer (so that divisors and sigma(n) are well-defined)
    try:
        if isinstance(witness, bool):
            h1 = False
        elif not isinstance(witness, (int, sympy.Integer)):
            h1 = False
        else:
            n = int(witness)
            h1 = (n != 0)
    except Exception:
        h1 = False

    # ¬Q: The conclusion \sum_{d|n} 1/d = \sigma(n)/n FAILS
    try:
        n = int(witness)
        divs = sympy.divisors(n)
        
        # Sum of reciprocals of positive divisors
        sum_recip = sum(sympy.Rational(1, d) for d in divs)
        
        # Sum of positive divisors
        sigma_n = sum(divs)
        
        # Check if the identity holds
        q = (sum_recip == sympy.Rational(sigma_n, n))
        
        # We want the conclusion to fail
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a non-zero integer",
    "¬Q: sum_{d|n} 1/d != sigma(n)/n"
]

N_HYP = 1
NEG_Q_INDEX = 1