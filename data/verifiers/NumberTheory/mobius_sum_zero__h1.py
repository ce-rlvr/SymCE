import sympy

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims that for any n, sum_{d|n} mu(d) = 1 if n = 1, and 0 if n > 1.
    (The dropped hypothesis is that n must be a positive integer).
    """
    try:
        # Evaluate the sum of the Möbius function over the divisors of the witness
        divs = sympy.divisors(witness)
        s = sum(sympy.mobius(d) for d in divs)
        
        # Safely check the conditions on n
        try:
            is_one = bool(witness == 1)
            is_gt_one = bool(witness > 1)
        except Exception:
            is_one = False
            is_gt_one = False
            
        # Check if the conclusion holds
        if is_one:
            q_holds = (s == 1)
        elif is_gt_one:
            q_holds = (s == 0)
        else:
            # If n < 1, the piecewise formula is either undefined or doesn't match the sum
            q_holds = False
            
    except Exception:
        # If divisors() or mobius() cannot be evaluated (e.g., for n=0 or non-integers),
        # the conclusion fails.
        q_holds = False

    neg_q = not q_holds
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: conclusion \\sum_{d|n} \\mu(d) = 1 if n = 1, and 0 if n > 1 fails"
]

N_HYP = 0
NEG_Q_INDEX = 0