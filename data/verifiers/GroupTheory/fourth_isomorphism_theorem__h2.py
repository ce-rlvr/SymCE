import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N) where G is a group and N is a subgroup.
    """
    try:
        if len(witness) != 2:
            return [False, False]
        G, N = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion fails
    try:
        if isinstance(G, PermutationGroup):
            # Ensure N is treated as a PermutationGroup
            if not isinstance(N, PermutationGroup):
                if isinstance(N, Permutation):
                    N = PermutationGroup([N])
                else:
                    N = PermutationGroup(list(N))
            
            # The conclusion of the Fourth Isomorphism Theorem holds if and only if N is normal in G.
            # If N is not a normal subgroup, G/N is not a group, so the conclusion fails.
            neg_q = not G.is_normal(N)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The conclusion fails (N is not a normal subgroup of G, so G/N is not a group)"
]

N_HYP = 1
NEG_Q_INDEX = 1