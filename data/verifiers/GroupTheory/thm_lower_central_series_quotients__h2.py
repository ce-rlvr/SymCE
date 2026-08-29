import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N, i).
    """
    try:
        G, N, i = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: i is a positive integer
    try:
        h2 = isinstance(i, int) and i > 0
    except Exception:
        h2 = False
        
    # ¬Q: The i-th term of the lower central series of G/N is NOT equal to (\gamma_i(G)N)/N
    # The conclusion mathematically holds if and only if N is a normal subgroup of G.
    # If N is not a normal subgroup (or not a subgroup at all), G/N is undefined as a group,
    # so the conclusion fails (neg_Q is True).
    try:
        if not isinstance(N, PermutationGroup):
            neg_q = True
        elif not N.is_subgroup(G):
            neg_q = True
        elif not N.is_normal(G):
            neg_q = True
        else:
            # N is a normal subgroup, so the theorem holds (conclusion is true, neg_Q is false)
            neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: i is a positive integer",
    "¬Q: The i-th term of the lower central series of G/N is not equal to (\\gamma_i(G)N)/N"
]

N_HYP = 2
NEG_Q_INDEX = 2