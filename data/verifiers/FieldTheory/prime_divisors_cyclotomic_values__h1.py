import sympy
from sympy.polys import cyclotomic_poly
from sympy import Symbol, isprime, Integer

# Top-level setup
x = Symbol('x')

def is_int(val):
    """Helper to check if a value is an integer (Python int or SymPy Integer)."""
    return isinstance(val, (int, Integer)) and not isinstance(val, bool)

def conditions(witness):
    """
    Given a witness tuple (a, n, p), checks if it is a valid counterexample.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        a, n, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: a is an integer
    try:
        h1 = is_int(a)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number dividing \Phi_n(a)
    # Note: The conjecture drops the "positive" prime requirement. 
    # A negative prime (e.g., p = -7 for n = 3, a = 2) can be a valid counterexample.
    try:
        if not is_int(p):
            h2 = False
        elif not isprime(abs(p)):
            h2 = False
        elif not (is_int(n) and n >= 1):
            h2 = False
        else:
            poly = cyclotomic_poly(int(n), x)
            phi_val = int(poly.subs(x, a))
            h2 = (phi_val % int(p) == 0)
    except Exception:
        h2 = False
        
    # ¬Q: p does not divide n AND p is not congruent to 1 mod n
    try:
        if not (is_int(n) and is_int(p) and p != 0 and n != 0):
            neg_q = False
        else:
            n_val = int(n)
            p_val = int(p)
            
            divides = (n_val % p_val == 0)
            equiv = ((p_val - 1) % n_val == 0)
            
            neg_q = not (divides or equiv)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: a is an integer",
    r"H_2: p is a prime number dividing \Phi_n(a)",
    r"¬Q: p does not divide n and p is not congruent to 1 mod n"
]

N_HYP = 2
NEG_Q_INDEX = 2