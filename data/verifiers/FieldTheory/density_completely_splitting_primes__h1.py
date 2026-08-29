import sympy

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The true theorem states that for any positive integer n, the Dirichlet density of primes
    splitting completely in the n-th cyclotomic field Q(zeta_n) is exactly 1/phi(n).
    If the hypothesis "n is a positive integer" is dropped, non-positive integers
    can serve as counterexamples where the conclusion fails (e.g., phi(n) is undefined or 
    the standard theorem does not apply).
    """
    n = None
    h1 = False
    
    try:
        # The witness can be just the integer n, or a tuple (K, n)
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            h1 = True
        elif isinstance(witness, tuple) and len(witness) == 2:
            _, n_val = witness
            if isinstance(n_val, (int, sympy.Integer)):
                n = int(n_val)
                h1 = True
    except Exception:
        h1 = False

    try:
        if h1 and n is not None:
            # For n > 0, the density is unconditionally 1/phi(n) by the Chebotarev Density Theorem.
            # For n <= 0, the conclusion fails.
            neg_q = (n <= 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K = Q(zeta_n) is the n-th cyclotomic field",
    "¬Q: The Dirichlet density of the set of prime numbers that split completely in K is not equal to 1/phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1