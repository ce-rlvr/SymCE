import sympy
from sympy.ntheory import factorint

# Top-level setup: named object bindings
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z10 = 10
Z12 = 12
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # Handle standard infinite domains where the nilradical is {0} (a prime ideal)
        if witness is sympy.ZZ or witness is sympy.QQ:
            h1 = True
            neg_q = False
            return [h1, neg_q]
            
        # Handle tuple or list of integers representing a direct product of Z_n rings
        if isinstance(witness, (tuple, list)) and len(witness) > 0:
            is_valid = True
            total_factors = 0
            for x in witness:
                val = int(x)
                if val < 2 or val > 10**9:
                    is_valid = False
                    break
                # The number of minimal prime ideals in Z_n is the number of distinct prime factors
                total_factors += len(factorint(val))
            
            if is_valid:
                h1 = True
                # In a direct product, the total number of minimal prime ideals is the sum of the 
                # number of minimal prime ideals of each factor.
                # The nilradical is prime (and the unique minimal prime ideal) iff there is exactly 1.
                neg_q = total_factors > 1
                return [h1, neg_q]
                
        # Handle single integer (representing Z_n) or a cyclic group (using its order)
        if hasattr(witness, 'order') and callable(witness.order):
            n = int(witness.order())
        else:
            n = int(witness)
            
        if 2 <= n <= 10**9:
            h1 = True
            factors = factorint(n)
            # In Z_n, the nilradical is prime iff n is a prime power (exactly 1 distinct prime factor)
            neg_q = len(factors) > 1
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The nilradical of R is not a prime ideal or is not the unique minimal prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1