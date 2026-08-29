import sympy

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it falsifies the conclusion of the conjecture.
    """
    # H_1: Let tau(n) denote the number of divisors of n
    # We interpret this as requiring the witness to be an integer.
    try:
        if isinstance(witness, bool):
            h1 = False
        else:
            n = int(witness)
            # Ensure it's exactly equal to its integer value (rejects non-integer floats/rationals)
            if n != witness:
                h1 = False
            else:
                h1 = True
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails at the witness
    try:
        if not h1:
            neg_q = False
        else:
            if n == 0:
                # For n = 0, the number of divisors is infinite, so the sums are undefined.
                # Thus, the equality sum_{d|n} tau(d)^3 == (sum_{d|n} tau(d))^2 fails to hold.
                neg_q = True
            else:
                # sympy.divisors returns the positive divisors of n
                divs = sympy.divisors(n)
                
                def tau(x):
                    return len(sympy.divisors(x))
                
                sum_cubes = sum(tau(d)**3 for d in divs)
                sum_tau = sum(tau(d) for d in divs)
                
                # neg_q is True if the conclusion FAILS
                neg_q = sum_cubes != sum_tau**2
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let tau(n) denote the number of divisors of n",
    "¬Q: sum_{d|n} tau(d)^3 != (sum_{d|n} tau(d))^2"
]

N_HYP = 1
NEG_Q_INDEX = 1