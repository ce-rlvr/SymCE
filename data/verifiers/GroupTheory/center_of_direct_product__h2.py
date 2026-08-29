import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # The witness must be a pair (G, H)
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # ¬Q: Z(G x H) is not equal to Z(G) x Z(H)
    try:
        # If H is not a group, the direct product and center operations are undefined,
        # meaning the equality Z(G x H) = Z(G) x Z(H) fails to hold.
        if not isinstance(H, PermutationGroup):
            neg_q_ok = True
        else:
            # If both are groups, compute the centers and their direct product
            GH = G * H
            Z_GH = GH.center()
            ZG = G.center()
            ZH = H.center()
            ZG_ZH = ZG * ZH
            
            # Check if they are isomorphic
            if Z_GH.order() != ZG_ZH.order():
                neg_q_ok = True
            else:
                neg_q_ok = not Z_GH.is_isomorphic(ZG_ZH)
    except Exception:
        # If any group operation fails, the conclusion's equality is undefined (hence false)
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: Z(G x H) is not equal to Z(G) x Z(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1