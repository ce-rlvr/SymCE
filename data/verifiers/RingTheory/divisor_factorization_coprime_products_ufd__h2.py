import sympy
from sympy import symbols, Integer, Rational, divisors

# Top-level setup
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a tuple of 3 elements: (a, b, d)
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        a, b, d = witness
        
        # Helper to check if an element is an integer
        def is_int(val):
            if isinstance(val, int):
                return True
            if hasattr(val, 'is_integer') and val.is_integer:
                return True
            return False
            
        # H_1: R is a UFD. We verify this by checking if the witness elements are integers,
        # since the ring of integers Z is a well-known UFD.
        h1 = is_int(a) and is_int(b) and is_int(d)
        if not h1:
            return [False, False, False]
            
        a, b, d = int(a), int(b), int(d)
        
        # H_2: d is a divisor of the product ab
        if d == 0:
            h2 = (a * b == 0)
        else:
            h2 = (a * b) % d == 0
            
        # ¬Q: The factorization d = d1 * d2 (where d1|a and d2|b) is NOT unique up to units.
        # In Z, units are 1 and -1. Two pairs (d1, d2) and (d1', d2') are equivalent up to units
        # if (d1', d2') == (d1, d2) or (d1', d2') == (-d1, -d2).
        if d == 0:
            # If d=0, d1*d2=0. This usually yields infinitely many valid pairs,
            # except in the highly degenerate cases where a=0, |b|=1 or b=0, |a|=1.
            if (a == 0 and abs(b) == 1) or (b == 0 and abs(a) == 1):
                neg_q = False
            else:
                neg_q = True
        else:
            divs = divisors(abs(d))
            valid_pairs = 0
            # By iterating only over positive divisors d1, we select exactly one 
            # representative for each unit-equivalence class of pairs (d1, d2).
            for d1 in divs:
                d2 = abs(d) // d1
                if d < 0:
                    d2 = -d2
                
                # Check if d1 divides a and d2 divides b
                if a % d1 == 0 and b % d2 == 0:
                    valid_pairs += 1
                    
            # The conclusion fails if there is not exactly 1 valid pair up to units
            neg_q = (valid_pairs != 1)
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain (witness elements are integers)",
    "H_2: d is a divisor of the product ab",
    "¬Q: The factorization d = d1 * d2 (where d1|a and d2|b) is not unique up to units"
]

N_HYP = 2
NEG_Q_INDEX = 2