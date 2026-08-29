import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G1 and G2 are groups
    try:
        h1 = isinstance(G1, PermutationGroup) and isinstance(G2, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N1 is a normal subgroup of G1
    try:
        h2 = isinstance(N1, PermutationGroup) and N1.is_subgroup(G1) and N1.is_normal(G1)
    except Exception:
        h2 = False
        
    # ¬Q: N1 x N2 is not a normal subgroup of G1 x G2
    # Mathematically, N1 x N2 is normal in G1 x G2 if and only if 
    # N1 is normal in G1 and N2 is normal in G2.
    try:
        if not (isinstance(N1, PermutationGroup) and isinstance(N2, PermutationGroup) and 
                isinstance(G1, PermutationGroup) and isinstance(G2, PermutationGroup)):
            neg_q = True
        else:
            n1_is_normal = N1.is_subgroup(G1) and N1.is_normal(G1)
            n2_is_normal = N2.is_subgroup(G2) and N2.is_normal(G2)
            neg_q = not (n1_is_normal and n2_is_normal)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G1 and G2 are groups",
    "H_2: N1 is a normal subgroup of G1",
    "¬Q: N1 x N2 is not a normal subgroup of G1 x G2"
]

N_HYP = 2
NEG_Q_INDEX = 2