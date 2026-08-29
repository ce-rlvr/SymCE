import math
import sympy

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple: (a, m, x, y)
    """
    try:
        a, m, x, y = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: a is an integer coprime to m
    try:
        h1 = (isinstance(a, (int, sympy.Integer)) and 
              isinstance(m, (int, sympy.Integer)) and 
              math.gcd(int(a), int(m)) == 1)
    except Exception:
        h1 = False
        
    # H2: x is the modular inverse of a modulo m
    try:
        h2 = False
        if isinstance(x, (int, sympy.Integer)):
            if m == 0:
                h2 = (a * x == 1)
            else:
                h2 = ((a * x) % m == 1 % m)
    except Exception:
        h2 = False
        
    # H3: y is the modular inverse of m - a modulo m
    try:
        h3 = False
        if isinstance(y, (int, sympy.Integer)):
            if m == 0:
                h3 = ((m - a) * y == 1)
            else:
                h3 = (((m - a) * y) % m == 1 % m)
    except Exception:
        h3 = False
        
    # Conclusion: x + y == 0 mod m
    # We evaluate the conclusion and negate it for the counterexample check.
    try:
        if m == 0:
            neg_q = (x + y != 0)
        else:
            neg_q = ((x + y) % m != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer coprime to m",
    "H_2: x is the modular inverse of a modulo m",
    "H_3: y is the modular inverse of m - a modulo m",
    "¬Q: x + y is not congruent to 0 modulo m"
]

N_HYP = 3
NEG_Q_INDEX = 3