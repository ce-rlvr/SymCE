import math

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture:
    "The number of k x k matrices with trace t modulo mn is the product of the number of such matrices modulo m and modulo n"
    
    Remaining hypotheses:
      - k is a positive integer
      - t is an integer
      - gcd(m, n) = 1
    """
    try:
        k, t, m, n = witness
    except Exception:
        return [False, False, False, False]

    # H_1: k is a positive integer
    try:
        h1 = isinstance(k, int) and k > 0
    except Exception:
        h1 = False

    # H_2: t is an integer
    try:
        h2 = isinstance(t, int)
    except Exception:
        h2 = False

    # H_3: gcd(m, n) = 1
    try:
        h3 = isinstance(m, int) and isinstance(n, int) and math.gcd(m, n) == 1
    except Exception:
        h3 = False

    # neg_Q: The conclusion fails at the witness
    try:
        # The number of k x k matrices with trace t modulo x is mathematically |x|^(k^2 - 1)
        # for any non-zero integer x. If x == 0, the number of such matrices over Z is infinite.
        def count_matrices(size, trace_val, mod):
            if mod == 0:
                return math.inf
            return abs(mod)**(size**2 - 1)

        count_mn = count_matrices(k, t, m * n)
        count_m = count_matrices(k, t, m)
        count_n = count_matrices(k, t, n)

        # The conclusion is that count_mn == count_m * count_n
        # neg_Q is True if this equality DOES NOT hold.
        neg_q = count_mn != count_m * count_n
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "H_2: t is an integer",
    "H_3: gcd(m, n) = 1",
    "¬Q: The number of matrices modulo mn is NOT the product of the number modulo m and modulo n"
]

N_HYP = 3
NEG_Q_INDEX = 3