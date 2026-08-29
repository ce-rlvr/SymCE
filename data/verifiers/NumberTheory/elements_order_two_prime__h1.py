import sympy
import math

def conditions(witness):
    """
    Given a witness (a, p), checks if it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            p = witness['p']
        else:
            a, p = witness
    except Exception:
        return [False, False]
    
    # H_1: a is an integer
    try:
        h1 = isinstance(a, (int, sympy.Integer))
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion FAILS at the witness
    # Conclusion: The order of a modulo p is exactly 2 iff a \equiv -1 \pmod p
    try:
        if not isinstance(p, (int, sympy.Integer)):
            neg_q = False
        elif p == 0:
            neg_q = False
        else:
            # Order is exactly 2 means a^2 \equiv 1 (mod p) and a \not\equiv 1 (mod p)
            side_a = (((a**2 - 1) % p) == 0) and (((a - 1) % p) != 0)
            # a \equiv -1 (mod p)
            side_b = (((a + 1) % p) == 0)
            
            # The conclusion is the biconditional (side_a == side_b)
            # We want the negation of the conclusion, so side_a != side_b
            neg_q = (side_a != side_b)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "¬Q: The order of a modulo p is exactly 2 if and only if a \\equiv -1 \\pmod p is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1