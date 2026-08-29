import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (n, N) where n is an integer and N is a PermutationGroup,
    or just a PermutationGroup N (in which case n is inferred from N.degree).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) != 2:
                return [False, False, False]
            n, N = witness
        else:
            N = witness
            n = N.degree
    except Exception:
        return [False, False, False]
        
    # H_1: Let n be an integer with n >= 5
    try:
        h1 = (int(n) == n) and (n >= 5)
    except Exception:
        h1 = False
        
    # H_2: Let S_n be the symmetric group on n letters (N is a subgroup of S_n)
    try:
        h2 = isinstance(N, PermutationGroup) and N.degree <= n
    except Exception:
        h2 = False
        
    # ¬Q: N is NOT the trivial subgroup, NOT the alternating group A_n, and NOT S_n
    try:
        order = N.order()
        fact = math.factorial(int(n))
        
        is_trivial = (order == 1)
        # For n >= 5, A_n is the unique subgroup of S_n of index 2
        is_An = (order == fact // 2)
        is_Sn = (order == fact)
        
        neg_q = not (is_trivial or is_An or is_Sn)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 5",
    "H_2: N is a subgroup of S_n",
    "¬Q: N is not the trivial subgroup, not A_n, and not S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2