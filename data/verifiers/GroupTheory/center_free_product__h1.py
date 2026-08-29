import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_order(grp):
    """Helper to safely get the order of a group whether it's a method or property."""
    o = grp.order
    return o() if callable(o) else o

def get_center(grp):
    """Helper to safely get the center of a group whether it's a method or property."""
    c = grp.center
    return c() if callable(c) else c

def conditions(witness) -> list[bool]:
    # The witness is expected to be a tuple of two groups: (G, H)
    try:
        G, H = witness
    except Exception:
        return [False, False, False]

    # H_1: H is a non-trivial group
    try:
        h1_ok = bool(get_order(H) > 1)
    except Exception:
        h1_ok = False

    # H_2: G * H is the free product of G and H
    # We verify this structural hypothesis by checking that G and H are valid group-like objects
    try:
        h2_ok = hasattr(G, 'order') and hasattr(H, 'order') and hasattr(G, 'center') and hasattr(H, 'center')
    except Exception:
        h2_ok = False

    # ¬Q: The center of G * H is NOT the trivial subgroup
    # Mathematically, the center of a free product G * H is trivial unless one of the groups is trivial
    # and the other has a non-trivial center.
    try:
        g_order = get_order(G)
        h_order = get_order(H)
        
        if g_order > 1 and h_order > 1:
            center_trivial = True
        elif g_order == 1:
            center_trivial = (get_order(get_center(H)) == 1)
        elif h_order == 1:
            center_trivial = (get_order(get_center(G)) == 1)
        else:
            center_trivial = True
            
        neg_q_ok = not center_trivial
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a non-trivial group",
    "H_2: G * H is the free product of G and H",
    "¬Q: The center of G * H is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2