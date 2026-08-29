import sympy
from sympy.ntheory import factorint
import math

# Top-level setup
# Witnesses are expected to be integers `m` (representing R=Z, I=mZ) 
# or tuples `(n, m)` (representing R=Z_n, I=mZ_n).
# No special named bindings are required for this domain.

def conditions(witness) -> list[bool]:
    try:
        # Parse the witness
        if isinstance(witness, (int, sympy.Integer)):
            n = 0
            m = int(witness)
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, m = witness
            n = int(n)
            m = int(m)
        else:
            return [False, False]
            
        # H_1: I is a two-sided ideal of R
        # In Z_n (or Z if n=0), any principal ideal mZ_n is a two-sided ideal 
        # because the ring is commutative.
        h1_ok = True
        
        # Q: R/I is a von Neumann regular ring
        # The quotient ring is Z_k where k = gcd(n, m) if n > 0 else abs(m)
        if n == 0:
            k = abs(m)
        else:
            k = math.gcd(n, m)
            
        # Check if Z_k is von Neumann regular
        # A ring Z_k is von Neumann regular iff k is square-free (for k > 0). 
        # Z_0 = Z is not von Neumann regular.
        if k == 0:
            q_ok = False
        elif k == 1:
            q_ok = True
        else:
            factors = factorint(k)
            q_ok = all(v == 1 for v in factors.values())
            
        neg_q_ok = not q_ok
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I is a two-sided ideal of R",
    "¬Q: The quotient ring R/I is not a von Neumann regular ring"
]

N_HYP = 1
NEG_Q_INDEX = 1