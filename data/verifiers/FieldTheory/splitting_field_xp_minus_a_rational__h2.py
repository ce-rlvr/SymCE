import sympy
from sympy import isprime, Rational, integer_nthroot
from sympy.abc import x

# Top-level setup for Field Theory / Number Theory
# No complex named objects are required for this specific conjecture,
# but we provide the standard symbol 'x' for polynomial context.

def conditions(witness) -> list[bool]:
    """
    Given a witness (p, a), checks if it is a valid counterexample to the conjecture.
    """
    try:
        p, a = witness
    except Exception:
        return [False, False]
        
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # ¬Q: The splitting field of x^p - a over Q does not have degree p(p-1) over Q
    try:
        a_rat = Rational(a)
        num, den = a_rat.p, a_rat.q
        
        def is_pth_power(n, p_val):
            if n == 0:
                return True
            if n < 0:
                if p_val % 2 == 0:
                    return False
                n = -n
            root, exact = integer_nthroot(n, p_val)
            return exact
            
        # Compute the actual degree of the splitting field of x^p - a over Q
        if a_rat == 0:
            actual_degree = 1
        elif is_pth_power(num, p) and is_pth_power(den, p):
            # a is a p-th power in Q, so x^p - a has a root in Q.
            # The splitting field is Q(zeta_p), which has degree p - 1.
            actual_degree = p - 1
        else:
            # a is not a p-th power in Q. Since p is prime, x^p - a is irreducible.
            # The splitting field is Q(a^{1/p}, zeta_p), which has degree p * (p - 1).
            actual_degree = p * (p - 1)
            
        expected_degree = p * (p - 1)
        neg_q = bool(actual_degree != expected_degree)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The splitting field of x^p - a over Q does not have degree p(p-1) over Q"
]

N_HYP = 1
NEG_Q_INDEX = 1