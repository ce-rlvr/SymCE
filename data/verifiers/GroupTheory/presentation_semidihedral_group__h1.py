import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness (the parameter n) satisfies the hypotheses and falsifies the conclusion.
    """
    try:
        # The presentation requires n to be an integer >= 1 so that 2^{n-1} is an integer.
        n = int(witness)
        h1 = (n >= 1) and (n == witness)
    except Exception:
        h1 = False

    try:
        # The conclusion is that G is isomorphic to the semidihedral group of order 2^{n+1}.
        # For n = 1, the presentation gives x^2=1, y^2=1, yxy=1 => x=1, so G is Z_2 (order 2 != 4).
        # For n = 2, the presentation gives x^4=1, y^2=1, yxy=x => xy=yx, so G is Z_4 x Z_2 (abelian).
        # Semidihedral groups are non-abelian and defined for order >= 16 (n >= 3).
        # Thus, the conclusion fails (neg_q is True) if and only if n < 3.
        n = int(witness)
        neg_q = (n < 3)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer >= 1 so the presentation is well-defined",
    "¬Q: G is not isomorphic to the semidihedral group of order 2^{n+1}"
]

N_HYP = 1
NEG_Q_INDEX = 1