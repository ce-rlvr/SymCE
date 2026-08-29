import sympy

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        # Ensure the witness is mathematically an integer
        if isinstance(witness, float) and not witness.is_integer():
            return [False, False]
        n = int(witness)
        if n != witness:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: There exists a non-negative integer k such that sigma(n) = 2^k
    try:
        if n == 0:
            h1 = False
        else:
            # sympy.divisor_sigma(n) computes the sum of divisors of |n|
            s = int(sympy.divisor_sigma(n))
            # Check if s is a power of 2 (i.e., s = 2^k for some non-negative integer k)
            h1 = bool(s > 0 and (s & (s - 1)) == 0)
    except Exception:
        h1 = False
        
    # neg_Q: n is NOT a product of distinct Mersenne primes
    try:
        if n <= 0:
            # A product of distinct Mersenne primes must be positive
            neg_q = True
        elif n == 1:
            # 1 is the empty product of distinct Mersenne primes
            neg_q = False
        else:
            factors = sympy.factorint(n)
            is_prod_mersenne = True
            for p, e in factors.items():
                if e > 1:
                    is_prod_mersenne = False
                    break
                if not sympy.isprime(p):
                    is_prod_mersenne = False
                    break
                # A Mersenne prime is of the form 2^m - 1, so p + 1 must be a power of 2
                if (p + 1) & p != 0:
                    is_prod_mersenne = False
                    break
            neg_q = not is_prod_mersenne
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: There exists a non-negative integer k such that sigma(n) = 2^k",
    "¬Q: n is not a product of distinct Mersenne primes"
]

N_HYP = 1
NEG_Q_INDEX = 1