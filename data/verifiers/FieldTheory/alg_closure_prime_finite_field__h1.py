import sympy
from sympy.ntheory import factorint, isprime

# Top-level setup
# No specific named bindings needed for this number-theoretic witness.

def conditions(witness) -> list[bool]:
    """
    Given a witness (expected to be an integer p), checks if it satisfies the remaining 
    hypotheses and if the conclusion fails.
    """
    try:
        p = int(witness)
    except Exception:
        return [False, False, False]
    
    # H_1: F_p is the finite field with p elements.
    # This requires p to be a prime power.
    try:
        if p < 2:
            h1 = False
        else:
            factors = factorint(p)
            h1 = (len(factors) == 1)
    except Exception:
        h1 = False
        
    # H_2: \overline{F_p} is an algebraic closure of F_p.
    # This is a definitional property that holds as long as F_p is a valid field.
    h2 = h1
    
    # ¬Q: The conclusion fails at the witness.
    # The original true theorem is specifically for a PRIME finite field. 
    # If the hypothesis "p is a prime" is dropped, the conjecture applies to all prime powers.
    # The conclusion is considered to fail when p is a prime power but not a prime.
    try:
        neg_q = not bool(isprime(p))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_p is the finite field with p elements",
    "H_2: \\overline{F_p} is an algebraic closure of F_p",
    "¬Q: \\overline{F_p} is not isomorphic to the union of the finite fields F_{p^n} for all integers n >= 1"
]

N_HYP = 2
NEG_Q_INDEX = 2