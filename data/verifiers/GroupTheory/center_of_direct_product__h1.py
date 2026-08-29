import sympy
from sympy.combinatorics import PermutationGroup, DirectProduct
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

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (G, H).
    """
    try:
        if not (isinstance(witness, (tuple, list)) and len(witness) == 2):
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: H is a group
    try:
        h1_ok = isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False

    # neg_Q: Z(G x H) != Z(G) x Z(H)
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            # If G or H is not a group, the equality of their centers is undefined/false.
            concl = False
        else:
            GxH = DirectProduct(G, H)
            Z_GxH = GxH.center()
            
            Z_G = G.center()
            Z_H = H.center()
            ZG_x_ZH = DirectProduct(Z_G, Z_H)
            
            # Check if they are the same group (same order and one is a subgroup of the other)
            concl = (Z_GxH.order() == ZG_x_ZH.order()) and Z_GxH.is_subgroup(ZG_x_ZH)
            
        neg_q = not concl
    except Exception:
        # If any group operation fails, the conclusion fails.
        neg_q = True

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group",
    "¬Q: Z(G x H) is not equal to Z(G) x Z(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1