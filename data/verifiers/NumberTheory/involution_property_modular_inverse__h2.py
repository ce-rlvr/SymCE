import sympy
import math

# No named bindings needed for Number Theory

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (a, n, x).
    """
    try:
        a, n, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: n is an integer strictly greater than 1
    try:
        h1 = isinstance(n, int) and n > 1
    except Exception:
        h1 = False
        
    # H2: \gcd(a, n) = 1
    try:
        try:
            g = sympy.gcd(a, n)
        except Exception:
            g = math.gcd(a, n)
        h2 = bool(g == 1)
    except Exception:
        h2 = False
        
    # H3: x is an integer such that ax \equiv 1 \pmod n
    try:
        h3 = isinstance(x, int) and bool((a * x) % n == 1)
    except Exception:
        h3 = False
        
    # neg_Q: The modular inverse of x modulo n is NOT congruent to a \pmod n
    try:
        # If x is not coprime to n, it has no modular inverse, so the conclusion fails.
        if math.gcd(x, n) != 1:
            neg_q = True
        else:
            inv_x = sympy.mod_inverse(x, n)
            neg_q = bool((inv_x % n) != (a % n))
    except Exception:
        # If we cannot compute the inverse or the modulo operation fails, the conclusion fails.
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: gcd(a, n) = 1",
    "H_3: x is an integer such that ax = 1 (mod n)",
    "¬Q: The modular inverse of x modulo n is not congruent to a (mod n)"
]

N_HYP = 3
NEG_Q_INDEX = 3