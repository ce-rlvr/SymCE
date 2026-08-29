import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension of fields with Galois group G",
    "H_2: H_1 and H_2 are subgroups of G",
    "¬Q: The fixed field of the intersection H_1 \\cap H_2 is not the compositum L^{H_1} L^{H_2}"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G, H1, H2 = witness
    except Exception:
        return [False, False, False]
    
    # H_1: L/K is a finite Galois extension of fields with Galois group G
    try:
        h1_ok = getattr(G, 'is_Group', False) or hasattr(G, 'elements')
        if hasattr(G, 'is_finite'):
            h1_ok = h1_ok and G.is_finite
    except Exception:
        h1_ok = False

    # H_2: H_1 and H_2 are subgroups of G
    try:
        h2_ok = (getattr(H1, 'is_Group', False) and 
                 getattr(H2, 'is_Group', False) and 
                 H1.is_subgroup(G) and 
                 H2.is_subgroup(G))
    except Exception:
        h2_ok = False

    # ¬Q: The fixed field of the intersection H_1 \cap H_2 is not the compositum L^{H_1} L^{H_2}
    try:
        # By the Fundamental Theorem of Galois Theory:
        # The fixed field of H_1 \cap H_2 corresponds to the subgroup H_1 \cap H_2.
        # The compositum L^{H_1} L^{H_2} corresponds to the intersection of their Galois groups, 
        # which is also exactly H_1 \cap H_2.
        # Because both fields correspond to the exact same subgroup, they are always equal 
        # for any finite Galois extension. The mathematical statement is a tautology.
        elements1 = set(H1.elements)
        elements2 = set(H2.elements)
        intersection_elements = elements1.intersection(elements2)
        
        subgroup_fixed_field_elements = intersection_elements
        subgroup_compositum_elements = intersection_elements
        
        conclusion = (subgroup_fixed_field_elements == subgroup_compositum_elements)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]