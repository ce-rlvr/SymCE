import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    # Parse the witness. It can be a tuple (n, H) or just H.
    # H can be a PermutationGroup or a list of Permutations generating the group.
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, H = witness
            if isinstance(H, list):
                H = PermutationGroup(*H)
        else:
            if isinstance(witness, list):
                H = PermutationGroup(*witness)
            else:
                H = witness
            
            # Infer n from the order of H if not explicitly provided
            order = H.order()
            n = 5
            while math.factorial(n - 1) < order:
                n += 1
    except Exception:
        n = None
        H = None

    # H_1: Let n >= 5 be an integer
    try:
        h1 = isinstance(n, int) and n >= 5
    except Exception:
        h1 = False

    # H_2: Let S_n be the symmetric group on n letters, and H a subgroup of S_n
    try:
        # In SymPy, a PermutationGroup is a subgroup of S_n if its degree is <= n
        h2 = isinstance(H, PermutationGroup) and H.degree <= n
    except Exception:
        h2 = False

    # H_3: Assume that the index of H in S_n is exactly n
    try:
        # The order of S_n is n!, so the index is n! / |H|
        h3 = math.factorial(n) == H.order() * n
    except Exception:
        h3 = False

    # ¬Q: The subgroup H is NOT isomorphic to the symmetric group S_{n-1}
    try:
        Sn_1 = SymmetricGroup(n - 1)
        if hasattr(H, 'is_isomorphic'):
            q = H.is_isomorphic(Sn_1)
        else:
            # Fallback if is_isomorphic is not available in the SymPy version
            q = (H.order() == Sn_1.order())
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 5 is an integer",
    "H_2: H is a subgroup of S_n",
    "H_3: The index of H in S_n is exactly n",
    "¬Q: The subgroup H is not isomorphic to the symmetric group S_{n-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3