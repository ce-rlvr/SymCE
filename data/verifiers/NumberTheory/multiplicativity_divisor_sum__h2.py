import sympy
from sympy import gcd, divisor_sigma

# Top-level setup for Number Theory
# (No named bindings needed; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        m, n = witness
    except Exception:
        return [False, False, False]
    
    # H1: m is a positive integer
    try:
        h1 = isinstance(m, (int, sympy.Integer)) and m > 0
    except Exception:
        h1 = False
        
    # H2: \gcd(m, n) = 1
    try:
        h2 = bool(gcd(m, n) == 1)
    except Exception:
        h2 = False
        
    # neg_Q: \sigma(mn) != \sigma(m)\sigma(n)
    try:
        # The sum of divisors function is standardly defined only for positive integers.
        # If n is not a positive integer, the conclusion is undefined and thus fails.
        def sigma(x):
            if not isinstance(x, (int, sympy.Integer)):
                raise ValueError("sigma is only defined for integers")
            if x <= 0:
                raise ValueError("sigma is only defined for positive integers")
            return divisor_sigma(x)
            
        lhs = sigma(m * n)
        rhs = sigma(m) * sigma(n)
        neg_q = bool(lhs != rhs)
    except Exception:
        # If evaluating sigma raises an exception (e.g., n <= 0), the conclusion fails.
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: m is a positive integer",
    r"H_2: \gcd(m, n) = 1",
    r"¬Q: \sigma(mn) \neq \sigma(m)\sigma(n) or is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2