import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        n = int(witness)
        if n < 2:
            return [False]
            
        # For R = Z/nZ, an R-algebra automorphism of R[x]/<x^2> is determined by x |-> ax + b.
        # This requires a to be a unit in R, and b to satisfy 2ab = 0 and b^2 = 0.
        # Since a is a unit, 2ab = 0 is equivalent to 2b = 0.
        # Thus, the automorphisms correspond to pairs (a, b) where a is in R^x and b is in B,
        # with B = {b in R | 2b = 0 and b^2 = 0}.
        # The size of the automorphism group is |R^x| * |B|.
        # For the group to be isomorphic to R^x, we must have |B| = 1 (so B = {0}).
        # In Z/nZ, 2b = 0 implies b = 0 or b = n/2 (if n is even).
        # If n is a multiple of 4, b = n/2 is a non-zero element and b^2 = n^2/4 = n*(n/4) = 0 mod n.
        # Therefore, |B| > 1 if and only if n is a multiple of 4.
        # When |B| > 1, the automorphism group is strictly larger than R^x, so they are not isomorphic.
        neg_q = (n % 4 == 0)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = ["¬Q: The group of R-algebra automorphisms of the dual numbers over R is not isomorphic to R^x"]

N_HYP = 0
NEG_Q_INDEX = 0