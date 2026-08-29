import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, N), checks if it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        # The witness must provide both the group G and the subgroup N
        G, N = witness
    except Exception:
        return [False, False]
    
    # H_1: G is a group (and N is a subgroup of G)
    try:
        h1_ok = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and N.is_subgroup(G)
    except Exception:
        h1_ok = False
        
    # ¬Q: The conclusion fails at the witness.
    # The conclusion is the Fourth Isomorphism Theorem, which states that H ↦ H/N is a bijection 
    # between subgroups of G containing N and subgroups of G/N, preserving normality.
    # This theorem holds if and only if N is a normal subgroup of G.
    # If N is not normal in G, G/N is not a group, and the conclusion is false.
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            neg_q_ok = not G.is_normal(N)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group and N is a subgroup of G",
    "¬Q: The map H ↦ H/N is not a valid bijection preserving normality (fails because N is not normal in G)"
]

N_HYP = 1
NEG_Q_INDEX = 1