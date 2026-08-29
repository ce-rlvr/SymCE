import sympy
from sympy.ntheory import factorint

# Top-level setup for potential witnesses
Z6 = 6
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'characteristic'):
            c = witness.characteristic()
        elif hasattr(witness, 'char'):
            c = witness.char()
        else:
            c = int(witness)
            
        c = abs(c)
        
        if c == 0:
            neg_q = False
        else:
            factors = factorint(c)
            # A number is a prime power if it has exactly one prime factor.
            # If it has more than 1 distinct prime factor, it is not a prime power.
            # (Characteristic 1 has 0 prime factors, which is also not a prime power,
            # but standard counterexamples like Z6 have >1 prime factors).
            neg_q = len(factors) > 1 or c == 1
            
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The characteristic of R is not 0 and not a prime power"
]

N_HYP = 0
NEG_Q_INDEX = 0