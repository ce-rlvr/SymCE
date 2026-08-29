import sympy
import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be the rank `n` of the free abelian group.
    """
    try:
        # H_1: n is a valid rank for a free abelian group.
        # It can be a non-negative integer or infinity.
        if witness == sympy.oo or witness == math.inf:
            h1 = True
        elif isinstance(witness, (int, sympy.Integer)) and witness >= 0:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        # ¬Q: The automorphism group of G is NOT isomorphic to GL(n, Z).
        # For finite n, Aut(Z^n) is isomorphic to GL(n, Z).
        # For infinite n, Aut(Z^n) is the group of column-finite invertible matrices,
        # which is strictly larger than the direct limit GL(n, Z).
        if witness == sympy.oo or witness == math.inf:
            neg_q = True
        elif isinstance(witness, (int, sympy.Integer)) and witness >= 0:
            neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a valid rank for a free abelian group (non-negative integer or infinity)",
    "¬Q: The automorphism group of G is not isomorphic to GL(n, Z)"
]

N_HYP = 1
NEG_Q_INDEX = 1