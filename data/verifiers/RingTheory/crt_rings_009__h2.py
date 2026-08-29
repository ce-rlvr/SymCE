import math
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I and J are ideals of R",
    "H_3: I + J = R",
    "¬Q: M/((I \\cap J)M) is not isomorphic to M/IM \\times M/JM"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Expected witness format:
    A tuple (a, b, n, A) or a dictionary with these keys, representing:
    - R = Z (the ring of integers)
    - I = aZ, J = bZ (ideals of Z)
    - M = Z/nZ (an abelian group)
    - A is the action of 1 in Z on M (i.e., 1 * m = A * m mod n)
    
    For M to be a valid Z-module, we must have A^2 == A mod n.
    A unitary module has A = 1. A non-unitary module can have A = 0.
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            n = witness['n']
            A = witness['A']
        else:
            if len(witness) != 4:
                return [False, False, False, False]
            a, b, n, A = witness
            
        a = int(a)
        b = int(b)
        n = int(n)
        A = int(A)
        
        if n < 1:
            return [False, False, False, False]
            
        # M must be a valid Z-module, meaning the action of 1 (which is A)
        # must satisfy 1 * 1 = 1, so A * A == A mod n.
        if (A * A) % n != A % n:
            return [False, False, False, False]
            
        # H1: R is a commutative ring with identity
        # R is implicitly Z, which satisfies this.
        h1 = True
        
        # H2: I and J are ideals of R
        # I = aZ and J = bZ are ideals of Z.
        h2 = True
        
        # H3: I + J = R
        # In Z, aZ + bZ = Z iff gcd(a, b) == 1.
        h3 = math.gcd(a, b) == 1
        
        # Conclusion: M/((I \cap J)M) \cong M/IM \times M/JM
        # We compute the sizes of these modules.
        # M = Z/nZ
        # IM = a * A * M, size of IM is n / gcd(n, a*A)
        # Size of M/IM is gcd(n, a*A)
        s_L = math.gcd(n, a * b * A)
        s_1 = math.gcd(n, a * A)
        s_2 = math.gcd(n, b * A)
        
        # Two finite cyclic groups are isomorphic iff they have the same size.
        # The RHS is a product of two cyclic groups of sizes s_1 and s_2.
        # It is isomorphic to the cyclic group LHS iff s_L == s_1 * s_2 
        # and gcd(s_1, s_2) == 1.
        isomorphic = (s_L == s_1 * s_2) and (math.gcd(s_1, s_2) == 1)
        
        neg_q = not isomorphic
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]