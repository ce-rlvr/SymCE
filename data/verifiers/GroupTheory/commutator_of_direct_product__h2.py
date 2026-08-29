import sympy
from sympy.combinatorics import PermutationGroup, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            G, H = witness
        else:
            G = witness
            H = None
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if H is None:
            neg_q = True
        else:
            LHS = DirectProduct(G, H).derived_subgroup()
            RHS = DirectProduct(G.derived_subgroup(), H.derived_subgroup())
            
            if LHS.is_subgroup(RHS) and RHS.is_subgroup(LHS):
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The commutator subgroup (G × H)' is not equal to G' × H'"
]

N_HYP = 1
NEG_Q_INDEX = 1