import math
import sympy
from sympy import Integer, Rational
from sympy.ntheory import factorint

# Top-level setup
# No specific named objects required for this number theory conjecture

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the conjecture:
    "There exist integers x and y such that p = x^2 + 2y^2 if and only if p ≡ 1 (mod 8) or p ≡ 3 (mod 8)"
    """
    try:
        # Ensure the witness is an integer
        if isinstance(witness, bool):
            return [False]
        if isinstance(witness, (int, Integer)):
            p = int(witness)
        else:
            p = int(witness)
            if p != witness:
                return [False]
    except Exception:
        return [False]
    
    try:
        # Condition A: There exist integers x, y such that p = x^2 + 2y^2.
        # A non-negative integer p can be represented by the quadratic form x^2 + 2y^2
        # if and only if every prime factor q ≡ 5, 7 (mod 8) has an even exponent in 
        # the prime factorization of p.
        if p < 0:
            A = False
        elif p == 0:
            A = True
        else:
            A = True
            factors = factorint(p)
            for q, exp in factors.items():
                if (q % 8 == 5 or q % 8 == 7) and exp % 2 != 0:
                    A = False
                    break
    except Exception:
        A = False

    try:
        # Condition B: p ≡ 1 (mod 8) or p ≡ 3 (mod 8)
        B = (p % 8 == 1) or (p % 8 == 3)
    except Exception:
        B = False

    try:
        # The conclusion is A <==> B.
        # The negated conclusion is that A is NOT equivalent to B.
        neg_Q = (A != B)
    except Exception:
        neg_Q = False

    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: (p = x^2 + 2y^2) is not equivalent to (p ≡ 1 or 3 mod 8)"
]

N_HYP = 0
NEG_Q_INDEX = 0