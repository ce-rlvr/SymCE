import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (G, H1, H2)
    where G is the Galois group (a PermutationGroup), and H1, H2 are subgroups corresponding 
    to the intermediate fields E_1 and E_2.
    """
    try:
        G = witness[0]
        H1 = witness[1]
        H2 = witness[2]
    except Exception:
        return [False, False, False]
        
    # H_1: K/F is a finite Galois extension with Galois group G
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: E_1 and E_2 are intermediate fields between F and K
    try:
        if isinstance(H1, list):
            H1 = PermutationGroup(H1)
        if isinstance(H2, list):
            H2 = PermutationGroup(H2)
        h2_ok = H1.is_subgroup(G) and H2.is_subgroup(G)
    except Exception:
        h2_ok = False
        
    # ¬Q: The subgroup of G corresponding to the compositum field E_1 E_2 is not the intersection of the subgroups H_1 \cap H_2.
    try:
        if not (isinstance(H1, PermutationGroup) and isinstance(H2, PermutationGroup)):
            neg_q = False
        else:
            # By the Fundamental Theorem of Galois Theory, the subgroup corresponding to the 
            # compositum field E_1 E_2 is exactly the intersection H_1 \cap H_2.
            # The conclusion claims that it is H_1 \cap H_2, which is unconditionally true.
            # Therefore, the conclusion never fails, and its negation is always False.
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: K/F is a finite Galois extension with Galois group G",
    "H_2: E_1 and E_2 are intermediate fields between F and K",
    "¬Q: The subgroup of G corresponding to the compositum field E_1 E_2 is not the intersection of the subgroups H_1 \\cap H_2"
]

N_HYP = 2
NEG_Q_INDEX = 2