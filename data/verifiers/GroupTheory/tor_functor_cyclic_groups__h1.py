import math
import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: Z_m and Z_n are cyclic groups of order m and n respectively",
    "¬Q: Tor_1(Z_m, Z_n) is not isomorphic to Z_gcd(m, n)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Parse the witness as a tuple of two integers (m, n)
        if isinstance(witness, (int, float)):
            m = n = int(witness)
        elif hasattr(witness, 'is_Integer') and witness.is_Integer:
            m = n = int(witness)
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            m = int(witness[0])
            n = int(witness[1])
        else:
            return [False, False]
            
        # H_1: Z_m and Z_n are cyclic groups of order m and n respectively.
        # In the context of Z-modules, Z_k has order ideal (k), so we accept any non-negative integers.
        # The dropped hypothesis from the true theorem is that the groups are FINITE (i.e., m, n > 0).
        h1 = (m >= 0 and n >= 0)
        
        # Evaluate the conclusion: Tor_1(Z_m, Z_n) is isomorphic to Z_gcd(m, n)
        # For any flat module (like Z_0 = Z), Tor_1 is 0, so its order is 1.
        # Otherwise, the order of Tor_1(Z_m, Z_n) is gcd(m, n).
        if m == 0 or n == 0:
            tor_order = 1
        else:
            tor_order = math.gcd(m, n)
            
        g = math.gcd(m, n)
        
        if g == 0:
            # gcd(0, 0) = 0. Z_0 = Z has infinite order, while Tor_1 has order 1.
            concl = False
        else:
            # Z_g has order g. Tor_1 has order tor_order.
            # They are isomorphic if and only if their orders match.
            concl = (tor_order == g)
            
        return [h1, not concl]
    except Exception:
        return [False, False]