import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for Number Theory
# No specific named bindings needed; use integers or rationals directly.

def conditions(witness) -> list[bool]:
    """
    Given a witness (a, p) or {'a': a, 'p': p}, checks if it is a valid counterexample
    to the false conjecture:
    "If p is a prime number, then gcd(a, p) = p if p divides a, and gcd(a, p) = 1 if p does not divide a."
    (The dropped hypothesis is that a must be an integer).
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            p = witness['p']
        else:
            a, p = witness
    except Exception:
        return [False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails at the witness
    try:
        a_sym = sympy.S(a)
        p_sym = sympy.S(p)
        
        # Check if p divides a (over integers)
        q = a_sym / p_sym
        if hasattr(q, 'is_integer') and q.is_integer is not None:
            p_divides_a = bool(q.is_integer)
        else:
            p_divides_a = bool(a_sym % p_sym == 0)
            
        gcd_val = sympy.gcd(a_sym, p_sym)
        
        if p_divides_a:
            conclusion = (gcd_val == p_sym)
        else:
            conclusion = (gcd_val == 1)
            
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: p divides a but gcd(a, p) != p, or p does not divide a but gcd(a, p) != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1