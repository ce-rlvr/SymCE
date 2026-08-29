import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The true theorem states that the *permutation* wreath product of S_m and S_n 
    embeds into S_{mn}. By dropping the word "permutation", the conjecture refers 
    to the *regular* wreath product of the abstract groups S_m and S_n.
    """
    try:
        if isinstance(witness, dict):
            m = witness['m']
            n = witness['n']
        else:
            m, n = witness
    except Exception:
        return [False, False]
        
    # H_1: m and n are positive integers
    try:
        h1 = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0
    except Exception:
        h1 = False
        
    # ¬Q: The regular wreath product S_m \wr S_n is NOT isomorphic to a subgroup of S_{mn}
    try:
        if not h1:
            neg_q = False
        else:
            # The regular wreath product of S_m and S_n has order (m!)^{n!} * n!
            # It is a subgroup of S_{mn} if and only if m=1, n=1, or n=2.
            # For m >= 2 and n >= 3, its order either does not divide (mn)! or is strictly greater,
            # making it impossible to be a subgroup of S_{mn}.
            neg_q = (m >= 2 and n >= 3)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: The wreath product S_m \\wr S_n is not isomorphic to a subgroup of S_{mn}"
]

N_HYP = 1
NEG_Q_INDEX = 1