import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def is_dp_nonabelian_simple(G):
    """
    Checks if a finite group G is isomorphic to a direct product of non-abelian simple groups.
    A finite group is a direct product of non-abelian simple groups iff it is perfect
    and has a trivial center. (The trivial group is the empty direct product).
    """
    try:
        if not hasattr(G, 'order'):
            return False
        order = G.order()
        if order == 1:
            return True
        if not hasattr(G, 'derived_subgroup'):
            return False
        # A direct product of non-abelian simple groups must be perfect
        if G.derived_subgroup().order() != order:
            return False
        # It must also have a trivial center
        if G.center().order() != 1:
            return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        # The witness must be a tuple of two groups (G_1, G_2)
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G1, G2 = witness
    except Exception:
        return [False, False]
    
    # H_1: G_1 is a finite group that is isomorphic to a direct product of non-abelian simple groups
    try:
        h1 = is_dp_nonabelian_simple(G1)
    except Exception:
        h1 = False
        
    # ¬Q: The direct product G_1 \times G_2 is NOT isomorphic to a direct product of non-abelian simple groups.
    # Mathematically, G_1 \times G_2 is a direct product of non-abelian simple groups 
    # if and only if BOTH G_1 and G_2 are.
    try:
        q = is_dp_nonabelian_simple(G1) and is_dp_nonabelian_simple(G2)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G_1 is a finite group that is isomorphic to a direct product of non-abelian simple groups",
    "¬Q: The direct product G_1 \\times G_2 is not isomorphic to a direct product of non-abelian simple groups"
]

N_HYP = 1
NEG_Q_INDEX = 1