import math
import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has a multiplicative identity",
    "H_3: x is a nilpotent element in R",
    "¬Q: The sum u + x is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample to the false conjecture.
    The witness is expected to represent a ring R (either Z or Z/nZ), an element u, and an element x.
    Format can be a tuple (n, u, x) where n is the modulo (0 for Z), or (u, x) assuming R = Z.
    """
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 3:
                n, u, x_val = witness
            elif len(witness) == 2:
                n = 0
                u, x_val = witness
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            n = witness.get('R', witness.get('n', 0))
            u = witness.get('u', 0)
            x_val = witness.get('x', 0)
        else:
            return [False, False, False, False]
            
        # Handle sympy domains
        if n == ZZ or str(n) in ['Z', 'ZZ']:
            n = 0
            
        # Evaluate conditions based on the ring Z/nZ (or Z if n=0)
        if isinstance(n, int) or (hasattr(n, 'is_integer') and n.is_integer):
            n = int(n)
            u = int(u)
            x_val = int(x_val)
            
            if n == 0:
                # Ring is Z
                h1 = True  # Z is a commutative ring
                h2 = True  # Z has a multiplicative identity (1)
                h3 = (x_val == 0)  # 0 is the only nilpotent element in Z
                neg_q = (abs(u + x_val) != 1)  # Units in Z are 1 and -1
                
            elif n >= 2:
                # Ring is Z/nZ
                h1 = True  # Z/nZ is a commutative ring
                h2 = True  # Z/nZ has a multiplicative identity (1)
                
                # x is nilpotent in Z/nZ iff x^k = 0 mod n for some k.
                # The index of nilpotency is always <= n, so x^n = 0 mod n is necessary and sufficient.
                h3 = (pow(x_val, n, n) == 0)
                
                # u + x is a unit in Z/nZ iff gcd(u + x, n) == 1
                neg_q = (math.gcd((u + x_val) % n, n) != 1)
                
    except Exception:
        pass

    return [h1, h2, h3, neg_q]