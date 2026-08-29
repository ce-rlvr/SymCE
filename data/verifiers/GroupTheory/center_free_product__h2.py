import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple of two groups (G, H).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    def get_order(g):
        o = g.order
        return o() if callable(o) else o

    def center_is_trivial(g):
        c = g.center
        c_val = c() if callable(c) else c
        return get_order(c_val) == 1

    # H_1: G is a non-trivial group
    try:
        h1_ok = isinstance(G, PermutationGroup) and get_order(G) > 1
    except Exception:
        h1_ok = False

    # H_2: G * H is the free product of G and H
    # This structurally requires H to be a valid group to form the free product.
    try:
        h2_ok = isinstance(H, PermutationGroup)
    except Exception:
        h2_ok = False

    # ¬Q: The center of G * H is not the trivial subgroup
    try:
        if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)):
            neg_q_ok = False
        else:
            g_order = get_order(G)
            h_order = get_order(H)
            
            # The center of a free product G * H is trivial if both G and H are non-trivial.
            # If one is trivial, the free product is isomorphic to the other group,
            # so its center is isomorphic to the center of that other group.
            if g_order > 1 and h_order > 1:
                center_trivial = True
            elif g_order == 1:
                center_trivial = center_is_trivial(H)
            elif h_order == 1:
                center_trivial = center_is_trivial(G)
            else:
                center_trivial = True
                
            neg_q_ok = not center_trivial
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a non-trivial group",
    "H_2: G * H is the free product of G and H",
    "¬Q: The center of G * H is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2