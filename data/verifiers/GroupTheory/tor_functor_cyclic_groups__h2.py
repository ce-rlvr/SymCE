import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup for standard algebra objects
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
    "H_1: m and n are positive integers",
    "¬Q: Tor_1(Z_m, Z_n) is not isomorphic to the cyclic group of order gcd(m, n)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # The witness is expected to be a tuple (m, n)
        m, n = witness
    except Exception:
        return [False, False]
        
    try:
        # Check if m and n are positive integers
        is_m_int = isinstance(m, (int, sympy.Integer)) and not isinstance(m, bool)
        is_n_int = isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool)
        h1 = is_m_int and is_n_int and m > 0 and n > 0
        
        if h1:
            m_val = int(m)
            n_val = int(n)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            # Compute Tor_1^Z(Z_m, Z_n).
            # Using the free resolution 0 -> Z --(x m)--> Z -> Z_m -> 0,
            # Tor_1(Z_m, Z_n) is isomorphic to the kernel of the map Z_n --(x m)--> Z_n.
            # We compute the size of this kernel.
            kernel_size = sum(1 for x in range(n_val) if (m_val * x) % n_val == 0)
            
            # Since the kernel is a subgroup of the cyclic group Z_n, it is guaranteed to be cyclic.
            # Thus, it is isomorphic to the cyclic group of order gcd(m, n) if and only if
            # its size is exactly gcd(m, n).
            expected_size = math.gcd(m_val, n_val)
            
            is_isomorphic = (kernel_size == expected_size)
            
            # neg_q is True if the conclusion FAILS (i.e., it is NOT isomorphic)
            neg_q = not is_isomorphic
    except Exception:
        neg_q = False
        
    return [h1, neg_q]