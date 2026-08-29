import math
import sympy
from sympy import Integer, Rational

# Top-level setup
# (No named bindings needed for this number theory conjecture; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        # The witness must be an integer.
        if not isinstance(witness, (int, Integer)):
            return [False]
        
        n = int(witness)
        
        # Evaluate gcd(n, n! + 1)
        # math.factorial will raise ValueError for negative integers,
        # which is caught by the except block.
        fact = math.factorial(n)
        val = math.gcd(n, fact + 1)
        
        # The conclusion is gcd(n, n! + 1) == 1.
        # The negated conclusion is that this gcd is NOT 1.
        neg_q = bool(val != 1)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = ["¬Q: gcd(n, n! + 1) != 1"]
N_HYP = 0
NEG_Q_INDEX = 0