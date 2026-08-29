import sympy
from sympy.ntheory import factorint

# No specific named bindings needed for this number theory conjecture.

def conditions(witness):
    try:
        n = int(witness)
    except Exception:
        return [False]
    
    try:
        # A positive integer n has a primitive root if and only if 
        # n is 1, 2, 4, p^k, or 2p^k for some odd prime p and k >= 1.
        if n <= 0:
            has_pr = False
        elif n in (1, 2, 4):
            has_pr = True
        else:
            m = n // 2 if n % 2 == 0 else n
            if m % 2 == 0:
                has_pr = False
            else:
                f = factorint(m)
                has_pr = (len(f) == 1)
        
        # The conjecture claims n has a primitive root iff n is in {2, 4, p^k, 2p^k}
        # for some odd prime p and positive integer k.
        in_set = False
        if n in (2, 4):
            in_set = True
        elif n > 0:
            m = n // 2 if n % 2 == 0 else n
            if m % 2 != 0 and m > 1:
                f = factorint(m)
                if len(f) == 1:
                    in_set = True
                    
        # The conclusion fails if the actual truth value of having a primitive root
        # does not match the conjecture's condition.
        neg_q = (has_pr != in_set)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: n has a primitive root iff n is in {2, 4, p^k, 2p^k} for odd prime p and k >= 1"
]
N_HYP = 0
NEG_Q_INDEX = 0