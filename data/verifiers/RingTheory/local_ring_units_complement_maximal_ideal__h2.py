import sympy
from sympy.ntheory import factorint
import math

# Top-level setup
# We evaluate the ring R as Z/nZ.
# A witness is expected to be a tuple (n, M, x) or a dict with these keys,
# where n is an integer >= 2, M is a list/set of integers, and x is an integer.

def conditions(witness):
    try:
        # Unpack witness
        if isinstance(witness, dict):
            n = witness.get('n', witness.get('R'))
            M = witness['M']
            x = witness['x']
        elif hasattr(witness, 'n'):
            n = witness.n
            M = witness.M
            x = witness.x
        else:
            n, M, x = witness
            
        if hasattr(n, 'order') and callable(n.order):
            n = n.order()
        elif isinstance(n, (list, set, tuple)):
            n = len(n)
            
        n = int(n)
        
        # H1: R is a local ring with identity
        # Z/nZ is a local ring iff n = p^k for some prime p.
        if n < 2:
            h1 = False
        else:
            factors = factorint(n)
            h1 = len(factors) == 1
            
        # H2: x is an element of R that is not contained in M
        try:
            iter(M)
            if isinstance(M, str):
                M_list = [M]
            else:
                M_list = list(M)
        except TypeError:
            M_list = [M]
            
        M_mod = {int(m) % n for m in M_list}
        x_mod = int(x) % n
        
        h2 = x_mod not in M_mod
        
        # neg_Q: x is NOT a unit in R
        # In Z/nZ, x is a unit iff gcd(x, n) == 1
        neg_q = math.gcd(x_mod, n) != 1
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a local ring with identity",
    "H_2: x is an element of R that is not contained in M",
    "¬Q: x is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2