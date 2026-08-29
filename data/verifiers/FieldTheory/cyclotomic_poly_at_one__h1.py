import sympy
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims that for the n-th cyclotomic polynomial Phi_n(x),
    Phi_n(1) = p if n is a power of a prime p, and Phi_n(1) = 1 if n is divisible
    by at least two distinct primes.
    (The dropped hypothesis is n > 1, making n = 1 the counterexample).
    """
    try:
        n = int(witness)
    except Exception:
        return [False, False]
        
    # H_1: \Phi_n(x) is the n-th cyclotomic polynomial
    # This implicitly requires n to be a valid index (n >= 1).
    try:
        h1 = (n >= 1)
    except Exception:
        h1 = False
        
    # Conclusion: \Phi_n(1) = p if n is a power of a prime p, 
    # and \Phi_n(1) = 1 if n is divisible by at least two distinct primes.
    try:
        if n < 1:
            q_holds = True # Vacuously true or invalid, so we don't flag as counterexample
        else:
            val = sympy.cyclotomic_poly(n, x).subs(x, 1)
            factors = sympy.factorint(n)
            
            if len(factors) == 1:
                # n is a power of a prime p
                p = list(factors.keys())[0]
                q_holds = (val == p)
            elif len(factors) >= 2:
                # n is divisible by at least two distinct primes
                q_holds = (val == 1)
            else:
                # n == 1: it has 0 prime factors.
                # The piecewise formula fails to describe \Phi_1(1) = 0.
                # Thus, the conclusion as a complete evaluation fails.
                q_holds = False
    except Exception:
        q_holds = True
        
    return [h1, not q_holds]

CONDITION_LABELS = [
    "H_1: \\Phi_n(x) is the n-th cyclotomic polynomial (n >= 1)",
    "¬Q: \\Phi_n(1) is not correctly evaluated by the stated piecewise formula"
]

N_HYP = 1
NEG_Q_INDEX = 1