import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Standard group theory and linear algebra objects
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two integers (n, m) representing the 
    cyclic groups G = Z/nZ and H = Z/mZ.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        
        n, m = witness
        
        # H_1: G is the cyclic group Z/nZ (n must be an integer)
        h1 = isinstance(n, (int, sympy.Integer))
        
        # H_2: H is the cyclic group Z/mZ (m must be an integer)
        h2 = isinstance(m, (int, sympy.Integer))
        
        if not (h1 and h2):
            return [False, False, False]
            
        n = int(n)
        m = int(m)
        
        # Calculate the size of Hom(Z/nZ, Z/mZ)
        # A homomorphism f: Z/nZ -> Z/mZ is determined by f(1) = k in Z/mZ
        # such that n*k = 0 in Z/mZ.
        if m == 0:
            if n == 0:
                hom_size = float('inf')
            else:
                hom_size = 1
        else:
            hom_size = math.gcd(n, m)
            
        # Calculate the size of the target group Z/gcd(n,m)Z
        g = math.gcd(n, m)
        if g == 0:
            target_size = float('inf')
        else:
            target_size = g
            
        # Since both Hom(Z/nZ, Z/mZ) and Z/gcd(n,m)Z are cyclic groups,
        # they are isomorphic if and only if they have the same size.
        # The conclusion FAILS if their sizes are different.
        neg_q = (hom_size != target_size)
        
        return [True, True, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is the cyclic group Z/nZ",
    "H_2: H is the cyclic group Z/mZ",
    "¬Q: Hom(G, H) is not isomorphic to Z/gcd(n,m)Z"
]

N_HYP = 2
NEG_Q_INDEX = 2