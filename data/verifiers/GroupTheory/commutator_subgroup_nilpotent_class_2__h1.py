import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        h1_val = witness.is_nilpotent
        h1 = h1_val() if callable(h1_val) else h1_val
    except Exception:
        h1 = False
        
    try:
        h2_val = witness.nilpotency_class
        h2 = (h2_val() if callable(h2_val) else h2_val) == 2
    except Exception:
        h2 = False
        
    try:
        G_prime = witness.derived_subgroup()
        Z = witness.center()
        
        is_subgroup = G_prime.is_subgroup(Z)
        
        gp_order = G_prime.order() if callable(G_prime.order) else G_prime.order
        z_order = Z.order() if callable(Z.order) else Z.order
        
        is_not_identity = gp_order > 1
        is_not_whole = gp_order < z_order
        
        q = is_subgroup and is_not_identity and is_not_whole
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: The nilpotency class of G is exactly 2",
    "¬Q: The commutator subgroup G' is not a proper non-trivial subgroup of the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2