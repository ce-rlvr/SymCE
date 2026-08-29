import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, H, g, phi)
    where phi can be a callable, a dictionary, or directly the image element phi(g).
    """
    try:
        G, H, g, phi = witness
    except Exception:
        return [False, False, False]

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: g in G is an element of finite order
    try:
        h2 = bool(g in G and g.order() > 0)
    except Exception:
        h2 = False

    # ¬Q: The order of phi(g) in H is not finite or does not divide the order of g
    try:
        if callable(phi):
            img = phi(g)
        elif isinstance(phi, dict):
            img = phi[g]
        else:
            img = phi
            
        if img not in H:
            # If the image is not even in H, it's not a valid setup for the conclusion
            neg_q = False
        else:
            img_order = img.order()
            g_order = g.order()
            # The conclusion fails if the image order does not divide the element order
            neg_q = bool(g_order % img_order != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: g in G is an element of finite order",
    "¬Q: The order of phi(g) in H is not finite or does not divide the order of g"
]

N_HYP = 2
NEG_Q_INDEX = 2