import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import math

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative local ring with unique maximal ideal m",
    "¬Q: The quotient ring R/I is not a local ring or its unique maximal ideal is not m/I"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # We model the ring R as Z/nZ and the ideal I as kZ/nZ.
        # The witness is expected to be a tuple (n, k).
        if isinstance(witness, tuple) and len(witness) == 2:
            n, k = witness
        elif hasattr(witness, '__iter__') and not isinstance(witness, str):
            items = list(witness)
            if len(items) == 2:
                n, k = items
            else:
                return [False, False]
        else:
            # If a single integer is provided, assume it's n and I = R (k=1)
            n = witness
            k = 1
            
        n = abs(int(n))
        k = abs(int(k))
        
        # H_1: R = Z/nZ is a local ring.
        # A finite ring Z/nZ is local iff n = p^a for some prime p and a >= 1.
        f_n = sympy.ntheory.factorint(n)
        h1_ok = (n > 1) and (len(f_n) == 1)
        
        # Q: R/I is a local ring.
        # R/I is isomorphic to Z/dZ where d = gcd(n, k).
        # It is local iff d = p^b for some prime p and b >= 1.
        d = math.gcd(n, k)
        f_d = sympy.ntheory.factorint(d)
        is_local = (d > 1) and (len(f_d) == 1)
        
        neg_q_ok = not is_local
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]