import sympy
import sympy.ntheory

# No specific top-level bindings needed for this number theory conjecture.

def conditions(witness):
    try:
        p = int(witness)
    except Exception:
        return [False, False]
    
    try:
        h1 = bool(sympy.isprime(p) and p % 2 == 1)
    except Exception:
        h1 = False
        
    try:
        if p % 5 in (1, 4):
            q = (sympy.ntheory.legendre_symbol(5, p) == 1)
        elif p % 5 in (2, 3):
            q = (sympy.ntheory.legendre_symbol(5, p) == -1)
        else:
            # The theorem implies (5/p) is fully determined by these cases.
            # For p = 5, p % 5 == 0, which is not covered, so the formula fails.
            q = False
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "¬Q: The Legendre symbol (5/p) is not correctly described by the +/-1 and +/-2 mod 5 cases"
]

N_HYP = 1
NEG_Q_INDEX = 1