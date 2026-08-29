import math
import sympy

# Top-level setup
# No special named objects are needed for integers modulo n.

def conditions(witness):
    """
    Given a witness (expected to be a tuple (n, a) or a dict with keys 'n' and 'a'),
    evaluates the hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
        else:
            n, a = witness
    except Exception:
        return [False, False, False]
        
    # H_1: Z_n is the ring of integers modulo n
    # This implies n is an integer.
    try:
        h1 = isinstance(n, (int, sympy.Integer))
    except Exception:
        h1 = False
        
    # H_2: a is an element of Z_n
    # This implies a is an integer (representing an equivalence class).
    try:
        h2 = isinstance(a, (int, sympy.Integer))
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion FAILS
    # Conclusion: a is a unit in Z_n if and only if the greatest common divisor of a and n is 1.
    try:
        n_int = int(n)
        a_int = int(a)
        
        # Determine if 'a' is a unit in Z_n.
        # By standard definition, a unit is an invertible element in a ring with 1 != 0.
        # Z_n has 1 != 0 only when |n| != 1.
        # For n = 1 or -1, Z_n is the trivial ring where 1 == 0, so it has no units.
        if abs(n_int) == 1:
            a_is_unit = False
        elif n_int == 0:
            # Z_0 is isomorphic to Z. The only units in Z are 1 and -1.
            a_is_unit = (abs(a_int) == 1)
        else:
            # For |n| > 1, an element a is a unit iff gcd(a, n) == 1
            a_is_unit = (math.gcd(a_int, n_int) == 1)
            
        gcd_is_one = (math.gcd(a_int, n_int) == 1)
        
        # The conclusion is the logical biconditional (iff)
        conclusion = (a_is_unit == gcd_is_one)
        
        # We want the negated conclusion (True when the conjecture fails)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Z_n is the ring of integers modulo n",
    "H_2: a is an element of Z_n",
    "¬Q: a is a unit in Z_n if and only if the greatest common divisor of a and n is 1"
]

N_HYP = 2
NEG_Q_INDEX = 2