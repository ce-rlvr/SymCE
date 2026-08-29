import sympy
from sympy import Rational

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness):
    try:
        a, m, n = witness
    except Exception:
        return [False, False]
    
    try:
        # Check if a is an integer
        h1 = (int(a) == a) and not isinstance(a, bool)
    except Exception:
        h1 = False
        
    try:
        # Evaluate the left side of the iff statement
        left = (sympy.gcd(a, m * n) == 1)
        # Evaluate the right side of the iff statement
        right = (sympy.gcd(a, m) == 1 and sympy.gcd(a, n) == 1)
        # The conclusion is (left == right). The negation is (left != right).
        neg_q = bool(left != right)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "¬Q: gcd(a, mn) = 1 iff gcd(a, m) = 1 and gcd(a, n) = 1 does not hold"
]

N_HYP = 1
NEG_Q_INDEX = 1